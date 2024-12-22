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
    print(f'Running main with settings: {settings.module_name}')