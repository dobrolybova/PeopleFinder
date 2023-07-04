from pydantic import BaseModel


class Request(BaseModel):
    first_name: str
    last_name: str


class Response(BaseModel):
    name: str
    age: int
    id: str


class PeopleFinderResponse(BaseModel):
    name: str
    age: int
