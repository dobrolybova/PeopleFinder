from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    msisdn: Optional[str] = None
    city: Optional[str] = None


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
