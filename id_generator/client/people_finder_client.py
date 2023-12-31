from logging import getLogger

from aiohttp import ClientResponseError
from pydantic import ValidationError

from client.requester import Requester, ResponseData
from exceptions import BadGateway
from schemes import Request, PeopleFinderResponse
from utils import construct_url

logger = getLogger(__name__)


class PeopleFinderClient(Requester):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def send_request(self, url, method):
        try:
            response: ResponseData = await self.request(url=url, method=method)
        except ClientResponseError as ex:
            logger.error(f"Error during client request: {ex.message}")
            raise BadGateway(user_message=f"Error during client request: {ex.message}")
        logger.info(f"Response from client is received {response.json}")
        return response

    async def find_person(self, body: Request) -> list[dict]:
        url = construct_url(body)
        method = "GET"
        response = await self.send_request(url, method)
        persons = response.json.get("persons")
        if not persons:
            persons = []
        try:
            content = [PeopleFinderResponse(**r).model_dump() for r in persons]
        except ValidationError as ex:
            logger.error(f"Wrong response from people finder {ex.__repr__()}")
            raise BadGateway(user_message=f"Wrong response from people finder {ex.__repr__()}")
        return content
