from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = ""
    LOG_FORMAT: str = '%(asctime)s,%(levelname)-5s %(filename)s:%(funcName)s:%(lineno)-5d %(message)s'


class Client(BaseSettings):
    TIMEOUT: int = 10
    BASE_URI: str = "http://localhost:8080"

