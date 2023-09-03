import uuid
from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from starlette.responses import JSONResponse

from client.people_finder_client import PeopleFinderClient
from dependencies import get_people_finder_client
from exceptions import InternalServerError
from schemes import Request, Response

main_router = APIRouter(prefix="")

logger = getLogger(__name__)


@main_router.post("/find")
async def find(body: Request, *, client: PeopleFinderClient = Depends(get_people_finder_client)):
    finder_rsp = await client.find_person(body)
    for r in finder_rsp:
        r["id"] = str(uuid.uuid4())
    try:
        content = [Response(**r).model_dump() for r in finder_rsp]
    except ValidationError as ex:
        logger.error(f"Response is not matched to Response schema {ex.__repr__()}")
        raise InternalServerError(user_message=f"Response is not matched to Response schema {ex.__repr__()}")

    return JSONResponse(status_code=HTTPStatus.OK, content={"persons": content})

