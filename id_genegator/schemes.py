from pydantic import BaseModel


class Request(BaseModel):
    first_name: str
    last_name: str


class Response(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    msisdn: str
    city: str
    id: str


class PeopleFinderResponse(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    msisdn: str
    city: str