from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound
from starlette.responses import JSONResponse

from db_handler import DbHandler
from dependencies import db_handler

main_router = APIRouter(prefix="")

logger = getLogger(__name__)


@main_router.get("/find_person")
async def find(first_name: str | None = None,
               last_name: str | None = None,
               age: int | None = None,
               email: str | None = None,
               msisdn: str | None = None,
               city: str | None = None,
               db: DbHandler = Depends(db_handler)):
    try:
        response = await db.get_records(first_name=first_name,
                                        last_name=last_name,
                                        age=age,
                                        email=email,
                                        msisdn=msisdn,
                                        city=city)
        content = [r.model_dump() for r in response]
        return JSONResponse(status_code=HTTPStatus.OK, content={"persons": content})
    except NoResultFound:
        logger.error(f"Data not found in people finder")
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={})
