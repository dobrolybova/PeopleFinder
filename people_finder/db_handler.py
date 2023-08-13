from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from schemes import People

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

    async def add_record(self, record: dict[str, str | int]):
        async with self.async_session() as session:
            async with session.begin():
                session.add(People(**record))
                await session.commit()

    async def delete_record(self, record: dict[str, str | int]):
        async with self.async_session() as session:
            async with session.begin():
                await session.delete(People(**record))
                await session.commit()

    async def fill_db(self, records: list[dict[str, str | int]]):
        for record in records:
            await self.add_record(record)
