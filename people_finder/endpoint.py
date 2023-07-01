from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter
from fastapi import Request
from starlette.responses import JSONResponse

main_router = APIRouter(prefix="")

logger = getLogger(__name__)

# TODO: Should be in DB
data = {"Yulia": {"age": 33}}


@main_router.get("/find_person/{name}")
def find(name: str):
    value = data.get(name)
    if value is not None:
        value["name"] = name
        logger.info(f"People finder send data {value}")
        return JSONResponse(status_code=HTTPStatus.OK, content=value)
    logger.error(f"Data not found in people finder")
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={})

