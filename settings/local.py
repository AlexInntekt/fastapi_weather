from .base import *

import os

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_KEY', 'ad0ad2ac179bf0b21d34052cc212bf1e') # key should not be harcoded here
OPENWEATHERMAP_BASE_URL = os.getenv('OPENWEATHERMAP_BASE_URL', 'https://api.openweathermap.org/data/2.5/weather')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 's3-temporary-bucket-alex')
