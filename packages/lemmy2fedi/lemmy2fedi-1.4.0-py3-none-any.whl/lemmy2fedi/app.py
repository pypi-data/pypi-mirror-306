"""High level logic for lemmy2feed."""

import asyncio
import sys
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Annotated
from typing import Optional

import httpx
import msgspec.toml
import stamina
import typer
from httpx import AsyncClient
from loguru import logger as log
from minimal_activitypub import SearchType
from minimal_activitypub import Status
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import NetworkError
from minimal_activitypub.client_2_server import RatelimitError

from lemmy2fedi import __version__
from lemmy2fedi.collect import determine_attachment_hash
from lemmy2fedi.collect import get_hashtag_timeline
from lemmy2fedi.collect import read_community
from lemmy2fedi.config import Configuration
from lemmy2fedi.config import create_default_config
from lemmy2fedi.control import PostRecorder
from lemmy2fedi.publish import connect
from lemmy2fedi.publish import cross_post
from lemmy2fedi.publish import post_media

stamina.instrumentation.set_on_retry_hooks([])


@log.catch
async def main(config_path: Path, max_posts: int | None) -> None:
    """Read communities and post to fediverse account."""
    log.info(f"Welcome to Lemmy2Fedi({__version__})")

    if config_path.exists():
        with config_path.open(mode="rb") as config_file:
            config_content = config_file.read()
            config = msgspec.toml.decode(config_content, type=Configuration)

    else:
        config = await create_default_config()
        with config_path.open(mode="wb") as config_file:
            config_file.write(msgspec.toml.encode(config))
        print("Please review your config file, adjust as needed, and run lemmy2fedi again.")
        sys.exit(0)

    async with AsyncClient(http2=True, timeout=30) as client:
        try:
            instance: ActivityPub
            my_username: str
            instance, my_username = await connect(auth=config.fediverse, client=client)
        except NetworkError as error:
            log.info(f"Unable to connect to your Fediverse account with {error=}")
            log.opt(colors=True).info("<red><bold>Can't continue!</bold></red> ... Exiting")
            sys.exit(1)

        with PostRecorder(history_db_path=config.history_db_path) as recorder:
            statuses_posted: int = 0
            while True:
                for _i in range(config.max_crossposts):
                    await cross_post_lemmy(client=client, config=config, instance=instance, recorder=recorder)
                    statuses_posted += 1
                    if max_posts and (statuses_posted >= max_posts):
                        break

                # Boost timeline posts
                if max_reblogs := config.fediverse.max_reblog:
                    try:
                        await boost_statuses_with_hashtags(
                            instance=instance,
                            my_username=my_username,
                            recorder=recorder,
                            max_boosts=max_reblogs,
                            no_reblog_tags=config.fediverse.no_reblog_tags,
                            no_reblog_users=config.fediverse.no_reblog_users,
                            post_recorder=recorder,
                            client=client,
                            search_instance=config.fediverse.search_instance,
                            tags=config.fediverse.search_tags,
                        )
                    except NetworkError as error:
                        log.warning(f"We've encountered the following error when boosting statuses: {error}")

                recorder.prune(max_age_in_days=config.history_prune_age)

                if not config.run_continuously:
                    break

                if max_posts and (statuses_posted >= max_posts):
                    log.debug(f"We've created {statuses_posted} statuses. Stopping now.")
                    break

                wait_until = datetime.now(tz=UTC) + timedelta(seconds=config.delay_between_posts)
                log.opt(colors=True).info(
                    f"<dim>Waiting until {wait_until:%Y-%m-%d %H:%M:%S %z} "
                    f"({config.delay_between_posts}s) before checking again.</>"
                )
                await asyncio.sleep(delay=config.delay_between_posts)


async def cross_post_lemmy(
    client: AsyncClient,
    config: Configuration,
    instance: ActivityPub,
    recorder: PostRecorder,
) -> None:
    """Check lemmy for posts and cross post."""
    for community in config.communities:
        log.debug(f"Processing posts from {community=}")
        try:
            posts = await read_community(
                instance=community.domain_name,
                name=community.name,
                client=client,
                sort=community.sort,
                limit=community.limit,
            )
        except (httpx.ConnectError, httpx.HTTPError) as error:
            log.opt(colors=True).error(
                f"<red>Could not read community</> "
                f"<cyan>{community.domain_name}/c/{community.name}</><red> - got {error}</>"
            )
            break

        for post_dict in posts["posts"]:
            post = post_dict.get("post", {})

            if not recorder.is_duplicate(identifiers=[post.get("id"), post.get("url"), post.get("ap_id")]):
                media_id: str | None = None
                if post.get("url"):
                    media_id = await post_media(activity_pub=instance, post=post, client=client, post_recorder=recorder)

                if community.only_with_attachment and not media_id:
                    log.opt(colors=True).info(
                        f"<dim><red>Skipping</red> <cyan>{post.get('name')}</cyan> "
                        f"because it has no supported attachment - {post.get('ap_id', '')}</dim>"
                    )
                    recorder.log_post(id=post.get("id"))
                    continue

                media_ids: list[str] = []
                if media_id:
                    media_ids.append(media_id)

                await cross_post(activity_pub=instance, post=post, media_ids=media_ids, tags=community.tags)

                recorder.log_post(id=post.get("id"), url=post.get("url"), ap_id=post.get("ap_id"))

                return


async def boost_statuses_with_hashtags(  # noqa: PLR0913
    instance: ActivityPub,
    my_username: str,
    recorder: PostRecorder,
    max_boosts: int,
    no_reblog_tags: list[str],
    no_reblog_users: list[str],
    post_recorder: PostRecorder,
    client: AsyncClient,
    search_instance: str | None,
    tags: list[str],
) -> None:
    """Boost posts on home timeline."""
    retry_caller = stamina.AsyncRetryingCaller(attempts=3)
    max_id: str = recorder.get_setting(key="max-boosted-id")

    search_on: str = search_instance if search_instance else instance.instance

    statuses = await get_statuses_with_tags(search_instance=search_on, tags=tags)

    number_boosted: int = 0
    if statuses:
        for status in reversed(statuses):
            status_id = status.get("id")

            # Check for any reason to skip reblogging this status
            if recorder.is_duplicate(identifiers=[status_id, status.get("url"), status.get("ap_id")]):
                continue
            if (
                bot_status(status=status)
                or my_own_status(status=status, my_username=my_username)
                or no_attachments(status=status)
                or has_no_reblog_tag(status=status, no_reblog_tags=no_reblog_tags)
                or by_no_reblog_user(status=status, no_reblog_users=no_reblog_users)
            ):
                recorder.log_post(id=status_id, url=status.get("url"), ap_id=status.get("ap_id"))
                continue

            # Check Attachments haven't been boosted / rebloged yet
            attachment_hash: Optional[str] = None
            for attachment in status.get("media_attachments", []):
                attachment_hash = await determine_attachment_hash(url=attachment.get("url"), client=client)
                if post_recorder.is_duplicate(identifiers=[attachment_hash]):
                    log.opt(colors=True).info(
                        f"<dim><red>Not Boosting:</red> At least one attachment of status at "
                        f"<cyan>{status.get('url')}</cyan> has already been boosted or posted.</dim>"
                    )
                    recorder.log_post(id=status_id, url=status.get("url"), ap_id=status.get("ap_id"))
                    break

            # Do the actual reblog
            status_url = status.get("url")
            search_result = await instance.search(query=status_url, query_type=SearchType.STATUSES, resolve=True)
            status_to_reblog = search_result.get("statuses")[0] if search_result.get("statuses") else None
            if status_to_reblog:
                reblog_id = status_to_reblog.get("id")
                await retry_caller(NetworkError, instance.reblog, status_id=reblog_id)
                number_boosted += 1
                log.opt(colors=True).info(f"Boosted <cyan>{status_url}</>")
                recorder.log_post(
                    attachment_hash=attachment_hash,
                    id=status_id,
                    url=status.get("url"),
                    ap_id=status.get("ap_id"),
                )

                max_id = status_id

            if number_boosted >= max_boosts:
                break

        recorder.save_setting(key="max-boosted-id", value=max_id)


async def get_statuses_with_tags(search_instance: str, tags: list[str]) -> list[Status]:
    """Get statuses found on search_instance with tags."""
    statuses: list[Status] = []

    retry_caller = stamina.AsyncRetryingCaller(attempts=3)
    try:
        statuses = await retry_caller(NetworkError, get_hashtag_timeline, search_instance=search_instance, tags=tags)
    except NetworkError as error:
        log.opt(colors=True).info(f"<dim>encountered {error=}</dim>")
    except RatelimitError:
        log.opt(colors=True).info("<dim>We've been rate limited... waiting for 30 minutes</dim>")
        await asyncio.sleep(1800)

    return statuses


def by_no_reblog_user(status: Status, no_reblog_users: list[str]) -> bool:
    """Check if status was posted by a user in the no_reblog_users list."""
    if status.get("account", {}).get("acct") in no_reblog_users:
        log.opt(colors=True).info(
            f"<dim><red>Not Boosting</red> <cyan>{status.get('url', '')}</cyan> "
            f"because it was posted by a user in the no_reblog_users list</dim>"
        )
        return True

    return False


def has_no_reblog_tag(status: Status, no_reblog_tags: list[str]) -> bool:
    """Check if status contains any tag in the no_reblog_tags list."""
    status_tags: list[str] = [x["name"].casefold() for x in status.get("tags", [])]
    if any(no_reblog.casefold() in status_tags for no_reblog in no_reblog_tags):
        log.opt(colors=True).info(
            f"<dim><red>Not Boosting</red> <cyan>{status.get('url', '')}</cyan> "
            f"because it contains tags that are in the no_reblog_tags list</dim>"
        )
        return True

    return False


def no_attachments(status: Status) -> bool:
    """Check if the status as NO attachments."""
    if not len(status.get("media_attachments", [])):
        log.opt(colors=True).info(
            f"<dim><red>Not Boosting</red> <cyan>{status.get('url', '')}</cyan> "
            f"because it has no attachments / media</dim>"
        )
        return True

    return False


def my_own_status(status: Status, my_username: str) -> bool:
    """Check if the status was posted by myself."""
    if status.get("account", {}).get("username") == my_username:
        log.opt(colors=True).debug(
            f"<dim><red>Skipping</red> post from myself - <cyan>{status.get('url', '')}</cyan></dim>"
        )
        return True

    return False


def bot_status(status: Status) -> bool:
    """Check if status has been made by a bot account."""
    if status.get("account", {}).get("bot"):
        log.opt(colors=True).info(
            f"<dim><red>Not Boosting</red> <cyan>{status.get('url', '')}</cyan> because it was posted by a bot</dim>"
        )
        return True

    return False


def async_shim(
    config_path: Annotated[Path, typer.Argument(help="path to config file")],
    logging_config_path: Annotated[
        Optional[Path], typer.Option("-l", "--logging-config", help="Full Path to logging config file")
    ] = None,
    max_posts: Annotated[
        Optional[int], typer.Option(help="maximum number of posts and reblogs before quitting")
    ] = None,
) -> None:
    """Start async part."""
    if logging_config_path and logging_config_path.is_file():
        with logging_config_path.open(mode="rb") as log_config_file:
            logging_config = msgspec.toml.decode(log_config_file.read())

        for handler in logging_config.get("handlers"):
            if handler.get("sink") == "sys.stdout":
                handler["sink"] = sys.stdout

        log.configure(**logging_config)

    asyncio.run(main(config_path=config_path, max_posts=max_posts))


def typer_shim() -> None:
    """Run actual code."""
    try:
        typer.run(async_shim)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    typer.run(async_shim)
