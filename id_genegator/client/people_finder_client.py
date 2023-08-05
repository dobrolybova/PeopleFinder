from logging import getLogger

from aiohttp import ClientResponseError
from pydantic import ValidationError

from client.requester import Requester, ResponseData
from exceptions import BadGateway
from schemes import Request, PeopleFinderResponse

logger = getLogger(__name__)


class PeopleFinderClient(Requester):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def send_request(self, url, method):
        try:
            response: ResponseData = await self.request(url=url, method=method)
            logger.info(f"Response from client is received {response.json}")
        except ClientResponseError as ex:
            logger.error(f"Error during client request: {ex.message}")
            raise BadGateway(user_message=f"Error during client request: {ex.message}")
        return response

    async def find_person(self, body: Request) -> dict:
        url = f"/find_person?first_name={body.first_name}&last_name={body.last_name}"
        method = "GET"
        response = await self.send_request(url, method)
        try:
            # TODO: List should be returned
            people_finder_resp = PeopleFinderResponse(**response.json)
        except ValidationError as ex:
            logger.error(f"Wrong response from people finder {ex.__repr__()}")
            raise BadGateway(user_message=f"Wrong response from people finder {ex.__repr__()}")
        return people_finder_resp.dict()
