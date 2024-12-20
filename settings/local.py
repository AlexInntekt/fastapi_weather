from .base import *

import os

USE_S3_CACHE = os.getenv('USE_S3_CACHE', True)
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_KEY', 'ad0ad2ac179bf0b21d34052cc212bf1e') # key should not be hardcoded here, should stay in .env
OPENWEATHERMAP_BASE_URL = os.getenv('OPENWEATHERMAP_BASE_URL', 'https://api.openweathermap.org/data/2.5/weather')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 's3-temporary-bucket-alex')
CACHE_TTL = os.getenv('CACHE_TTL', 5)
DELETE_ALL_CACHED_FILES = os.getenv('DELETE_ALL_CACHED_FILES', True)
S3_REGION_NAME = os.getenv('S3_REGION_NAME', 'eu-central-1')