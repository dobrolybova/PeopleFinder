from time import time

from fastapi import Request, Response
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from metrics.metrics import SERVER_REQUEST_COUNT


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

            if status is None:
                response_status = "UNKNOWN"
            elif status < 400:
                response_status = "OK"
            elif status < 500:
                response_status = "CLIENT_ERROR"
            else:
                response_status = "SERVER_ERROR"
            SERVER_REQUEST_COUNT.labels(
                request.method, response_status, request.url, status
            ).observe(time() - start_time)


middleware_seq = [Middleware(Monitoring)]
