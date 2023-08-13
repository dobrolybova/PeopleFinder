from logging import getLogger
from typing import Sequence

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select

from schemes import People, PeopleResponse

logger = getLogger(__name__)

DATABASE = {
    'drivername': 'postgresql+asyncpg',
    'host': 'localhost',
    'port': '5432',
    'username': 'yulia',
    'password': 'yulia',
    'database': 'people',
    'query': {}
}


class DbHandler:
    def __init__(self):
        self.engine = create_async_engine(URL(**DATABASE), future=True, echo=True)
        self.async_session = async_sessionmaker(self.engine, class_=AsyncSession)

    async def add_record(self, record: dict[str, str | int]) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add(People(**record))
                await session.commit()

    async def delete_record(self, record: dict[str, str | int]) -> None:
        async with self.async_session() as session:
            async with session.begin():
                await session.delete(People(**record))
                await session.commit()

    async def get_record_by_full_name(self, first_name: str, last_name: str) -> PeopleResponse:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.first_name == first_name and
                                                                    People.last_name == last_name))
                row = result.one()
                return PeopleResponse(first_name=row.first_name,
                                      last_name=row.last_name,
                                      age=row.age,
                                      msisdn=row.msisdn,
                                      email=row.email,
                                      city=row.city)

    async def get_record_by_email(self, email: str) -> PeopleResponse:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.email == email))
                row = result.one()
                return PeopleResponse(first_name=row.first_name,
                                      last_name=row.last_name,
                                      age=row.age,
                                      msisdn=row.msisdn,
                                      email=row.email,
                                      city=row.city)

    async def get_record_by_msisdn(self, msisdn: str) -> PeopleResponse:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.msisdn == msisdn))
                row = result.one()
                return PeopleResponse(first_name=row.first_name,
                                      last_name=row.last_name,
                                      age=row.age,
                                      msisdn=row.msisdn,
                                      email=row.email,
                                      city=row.city)

    # TODO: return values for lists
    async def get_record_by_first_name(self, first_name: str) -> Sequence[People]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.first_name == first_name))
                return result.fetchall()

    async def get_record_by_last_name(self, last_name: str) -> Sequence[People]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.last_name == last_name))
                return result.fetchall()

    async def get_record_by_age(self, age: int) -> Sequence[People]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.age == age))
                return result.fetchall()

    async def get_record_by_city(self, city: int) -> Sequence[People]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.scalars(select(People).where(People.city == city))
                return result.fetchall()

    async def fill_db(self, records: list[dict[str, str | int]]) -> None:
        for record in records:
            await self.add_record(record)
