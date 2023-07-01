from logging import getLogger, basicConfig

import uvicorn as uvicorn
from fastapi import FastAPI, Depends

from config import Settings
from dependencies import log_incoming_body
from endpoint import main_router

settings = Settings()


logger = getLogger(__name__)
basicConfig(filename=settings.LOG_FILE, filemode='w', level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)

app = FastAPI()

app.include_router(main_router, dependencies=[Depends(log_incoming_body)])


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
