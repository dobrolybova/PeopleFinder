from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter
from starlette.responses import JSONResponse

main_router = APIRouter(prefix="")

logger = getLogger(__name__)

# TODO: Should be in DB
data = {"Ivan": {"age": 33}}


@main_router.get("/find_person")
def find(first_name: str = "", last_name: str = ""):
    value = data.get(first_name)
    if value is not None:
        value["name"] = first_name
        logger.info(f"People finder send data {value}")
        return JSONResponse(status_code=HTTPStatus.OK, content=value)
    logger.error(f"Data not found in people finder")
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={})

