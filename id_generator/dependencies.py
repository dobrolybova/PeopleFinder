from functools import lru_cache
from logging import getLogger

from fastapi import Request

from client.people_finder_client import PeopleFinderClient
from config import Client

logger = getLogger(__name__)
settings = Client()


@lru_cache
def get_people_finder_client() -> PeopleFinderClient:
    return PeopleFinderClient(settings.BASE_URI)


async def log_incoming_body(body: Request) -> None:
    req_body = await body.json()
    logger.info(f"New incoming request with body: {req_body}")
