from http import HTTPStatus
from time import time

from fastapi import Request, Response
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from metrics.metrics import SERVER_REQUEST


class Monitoring(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            if response is not None:
                status = response.status_code
            else:
                status = None
            SERVER_REQUEST.labels(
                request.method, request.url, status
            ).observe(time() - start_time)


middleware_seq = [Middleware(Monitoring)]
