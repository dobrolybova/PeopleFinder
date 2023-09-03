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

    async def get_records(self,
                          first_name: str | None = None,
                          last_name: str | None = None,
                          age: int | None = None,
                          email: str | None = None,
                          msisdn: str | None = None,
                          city: str | None = None) -> Sequence[PeopleResponse]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(People)
                # TODO: refactor
                if first_name is not None:
                    query = query.where(People.first_name == first_name)
                if last_name is not None:
                    query = query.where(People.last_name == last_name)
                if age is not None:
                    query = query.where(People.age == age)
                if email is not None:
                    query = query.where(People.email == email)
                if msisdn is not None:
                    query = query.where(People.msisdn == msisdn)
                if city is not None:
                    query = query.where(People.city == city)

                result = await session.scalars(query)
                raw = result.fetchall()
                return [PeopleResponse(first_name=elem.first_name,
                                       last_name=elem.last_name,
                                       age=elem.age,
                                       msisdn=elem.msisdn,
                                       email=elem.email,
                                       city=elem.city) for elem in raw]

    async def fill_db(self, records: list[dict[str, str | int]]) -> None:
        for record in records:
            await self.add_record(record)
