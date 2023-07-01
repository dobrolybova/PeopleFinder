from logging import getLogger

from fastapi import Request

logger = getLogger(__name__)


async def log_incoming_body(name: str) -> None:
    logger.info(f"New incoming request to people finder with param: {name}")
