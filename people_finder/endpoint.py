from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter
from sqlalchemy.exc import NoResultFound
from starlette.responses import JSONResponse

from db_handler import DbHandler

main_router = APIRouter(prefix="")

logger = getLogger(__name__)


# TODO: find by different attibutes
# TODO: DbHandler in dep
@main_router.get("/find_person")
async def find(first_name: str = "", last_name: str = ""):
    db = DbHandler()
    try:
        response = await db.get_record_by_full_name(first_name, last_name)
        return JSONResponse(status_code=HTTPStatus.OK, content=response.model_dump())
    except NoResultFound:
        logger.error(f"Data not found in people finder")
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={})
