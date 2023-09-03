from pydantic import BaseConfig


class AppSettings(BaseConfig):
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = ""
    LOG_FORMAT: str = '%(asctime)s,%(levelname)-5s %(filename)s:%(funcName)s:%(lineno)-5d %(message)s'
    DB_INIT_DATA_FILE_NAME: str = "db_data"
