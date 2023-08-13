from sqlalchemy import Integer, Column, Text
from sqlalchemy.orm import declarative_base

base = declarative_base()


class People(base):
    __tablename__ = "people"
    id = Column(Integer(), primary_key=True)
    first_name = Column(Text())
    last_name = Column(Text())
    age = Column(Integer())
    email = Column(Text())
    phone = Column(Text())
    city = Column(Text())

