import os

import psycopg2
from sqlalchemy.orm import declarative_base

sql_commands = (
        # """
        # CREATE USER yulia WITH SUPERUSER PASSWORD 'yulia'
        # """,
        """
        CREATE database people
        """,
)


def create_db(commands: tuple[str]):
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


def start_db():
    try:
        create_db(sql_commands)
    except psycopg2.errors.DuplicateDatabase:
        pass
    os.system("alembic upgrade head")


def fill_db_data():
    pass


if __name__ == "__main__":
    start_db()
