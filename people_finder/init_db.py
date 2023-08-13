import asyncio
import json
import os

import psycopg2
from sqlalchemy.orm import declarative_base

from db_handler import DbHandler

sql_commands_create = (
        # """
        # CREATE USER yulia WITH SUPERUSER PASSWORD 'yulia'
        # """,
        """
        CREATE database people
        """,
)

sql_commands_drop = (
        # """
        # DROP USER yulia WITH SUPERUSER PASSWORD 'yulia'
        # """,
        """
        DROP database people
        """,
)


def execute_db(commands: tuple[str]):
    conn = psycopg2.connect(database="postgres",
                            user="yulia",
                            password="yulia",
                            host="localhost",
                            port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    conn.close()


Base = declarative_base()


async def fill_db():
    # TODO: move file name to config
    with open("db_data.json") as fp:
        data = fp.read()
    json_list = []
    for elem in data.split("\n"):
        json_list.append(json.loads(elem))
    db = DbHandler()
    await db.fill_db(json_list)


def start_db():
    execute_db(sql_commands_drop)
    execute_db(sql_commands_create)
    os.system("alembic upgrade head")


async def task_f():
    await asyncio.create_task(fill_db())

if __name__ == "__main__":
    start_db()
    asyncio.run(task_f())
