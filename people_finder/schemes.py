from sqlalchemy import Integer, Column, Text
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

base = declarative_base()


class People(base):
    __tablename__ = "people"
    id = Column(Integer(), primary_key=True)
    first_name = Column(Text())
    last_name = Column(Text())
    age = Column(Integer())
    email = Column(Text())
    msisdn = Column(Text())
    city = Column(Text())


class PeopleResponse(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    msisdn: str
    city: str


