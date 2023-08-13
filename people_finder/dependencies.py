from logging import getLogger

logger = getLogger(__name__)


async def log_incoming_body(first_name: str = "", last_name: str = "") -> None:
    logger.info(f"New incoming request to people finder with first_name: {first_name} last_name: {last_name}")
