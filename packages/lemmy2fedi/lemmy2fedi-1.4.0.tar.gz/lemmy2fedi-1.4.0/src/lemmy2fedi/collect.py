"""Methods to collect information from Lemmy Instances."""

import json
from hashlib import sha256
from typing import Any

import httpx
import msgspec.json
import stamina
from httpx import AsyncClient
from loguru import logger as log
from minimal_activitypub import Status
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import NetworkError


@stamina.retry(on=(httpx.ConnectError, httpx.HTTPError), attempts=3)
async def read_community(instance: str, name: str, client: AsyncClient, sort: str = "Hot", limit: int = 10) -> Any:
    """Read lemmy community posts with sort on Hot."""
    url = f"https://{instance}/api/v3/post/list?limit={limit}&sort={sort}&community_name={name}"
    response = await client.get(url=url)
    log.debug(f"{instance}/c/{name} - {response.status_code} - {response.headers=}")
    response.raise_for_status()

    msgspec_response = msgspec.json.decode(response.content)

    return msgspec_response


@stamina.retry(on=NetworkError, attempts=3)
async def get_hashtag_timeline(search_instance: str, tags: list[str]) -> list[Status]:
    """Search for statuses with 'tags' on 'search_instance'."""
    first_tag = tags[0]
    any_other_tags = tags[1:] if len(tags) > 1 else None
    async with AsyncClient(http2=True, timeout=30) as client:
        search_on = ActivityPub(instance=search_instance, client=client)
        results: list[Status] = await search_on.get_hashtag_timeline(
            hashtag=first_tag,
            any_tags=any_other_tags,
            only_media=True,
            limit=40,
        )

    log.debug(f"results={json.dumps(results, indent=4)}")

    return results


async def determine_attachment_hash(url: str, client: AsyncClient) -> str:
    """Determine attachment hash."""
    response = await client.get(url=url)
    url_hash = sha256(response.content).hexdigest()
    return url_hash
