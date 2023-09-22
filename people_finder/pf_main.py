from logging import getLogger, basicConfig

import uvicorn as uvicorn
from fastapi import FastAPI, Depends

from pf_config import AppSettings
from pf_dependencies import log_incoming_body
from pf_endpoint import main_router

settings = AppSettings()


logger = getLogger(__name__)
basicConfig(filename=settings.LOG_FILE, filemode='w', level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)


app = FastAPI()

app.include_router(main_router, dependencies=[Depends(log_incoming_body)])


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
