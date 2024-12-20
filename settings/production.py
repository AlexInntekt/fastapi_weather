from .base import *

import os

USE_S3_CACHE = os.getenv('USE_S3_CACHE', True)
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_KEY')
OPENWEATHERMAP_BASE_URL = os.getenv('OPENWEATHERMAP_BASE_URL')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
DELETE_ALL_CACHED_FILES = os.getenv('DELETE_ALL_CACHED_FILES', True)
S3_REGION_NAME = os.getenv('S3_REGION_NAME', 'eu-central-1')

if not OPENWEATHERMAP_API_KEY:
    raise ValueError("The OPENWEATHERMAP_API_KEY setting is not configured.")

if not OPENWEATHERMAP_BASE_URL:
    raise ValueError("The OPENWEATHERMAP_BASE_URL setting is not configured.")

if not S3_BUCKET_NAME:
    raise ValueError("The S3_BUCKET_NAME setting is not configured.")
