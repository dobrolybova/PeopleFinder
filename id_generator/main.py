import uvicorn as uvicorn

from config import Settings
from dependencies import log_incoming_body
from metrics.handler import metrics_router
from endpoint import main_router
from fastapi.exceptions import RequestValidationError
from exceptions import (
    ServiceError,
    exc_handler,
    request_validation_exc_handler,
    service_error_exc_handler,
)
from fastapi import FastAPI, Depends
from middlewares import middleware_seq
from logging import getLogger, basicConfig

settings = Settings()

# TODO: put in Docker
logger = getLogger(__name__)
basicConfig(filename=settings.LOG_FILE, filemode='w', level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)

app = FastAPI(
    middleware=middleware_seq,
)

app.include_router(metrics_router)
app.include_router(main_router, dependencies=[Depends(log_incoming_body)])

app.add_exception_handler(ServiceError, service_error_exc_handler)
app.add_exception_handler(RequestValidationError, request_validation_exc_handler)
app.add_exception_handler(Exception, exc_handler)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
