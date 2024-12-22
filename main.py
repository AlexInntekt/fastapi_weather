import sys
import os
import time
import io

from fastapi import FastAPI

sys.path.append(os.getcwd())

import settings
from utils.logging import get_logger
from routes.routes import router


logger = get_logger(__name__)


app = FastAPI()
app.include_router(router)


if __name__=='__main__':
    logger.debug(f'Running main with settings: {settings.module_name}')

    # in case you dont want to use 'fastapi dev main.py', pipenv install uvicorn and then:
    # import uvicorn
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)