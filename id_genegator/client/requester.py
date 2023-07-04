import time
from dataclasses import dataclass
from functools import wraps
from logging import getLogger
from re import sub

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client import _RequestContextManager
from aiohttp.client_exceptions import ContentTypeError

from config import Client
from metrics.metrics import CLIENT_REQUEST

settings = Client()
logger = getLogger(__name__)


def record_request_metrics(coroutine):
    @wraps(coroutine)
    async def wrapped(*args, **kwargs):
        status = None
        req_start = time.time()
        try:
            ret = await coroutine(*args, **kwargs)
            status = ret.status
            return ret
        finally:
            req_elapsed_time = time.time() - req_start
            url = sub(r"\d{2,}", "{int}", kwargs.get("url", "None"))
            CLIENT_REQUEST.labels(
                kwargs.get("method"), url, status
            ).observe(req_elapsed_time)

    return wrapped


@dataclass
class DecodedResponse:
    status: int
    json: dict


class Requester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    def get_session(self, method, url, **kwargs) -> _RequestContextManager:
        if self.session is None or self.session.closed:
            self.session = ClientSession(
                timeout=ClientTimeout(total=settings.TIMEOUT),
                base_url=self.base_url)
        return self.session.request(method, url, **kwargs)

    @record_request_metrics
    async def request_decoded(
            self, method="GET", url="", exc_by_status=True, **kwargs
    ) -> DecodedResponse:
        async with self.get_session(method, url, **kwargs) as response:
            js = {}
            try:
                js = await response.json()
            except ContentTypeError as exc:
                text = await response.text()
                logger.info(f"exception: {exc} text: {text}")
            logger.info(f"Response received with "
                        f"status: {str(response.status)} "
                        f"method: {method} "
                        f"url: {str(response.url)} "
                        f"body: {js}")
            if exc_by_status:
                response.raise_for_status()
            return DecodedResponse(response.status, js)
