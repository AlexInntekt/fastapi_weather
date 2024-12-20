import os

CACHE_TTL = os.getenv('CACHE_TTL', 5)
USE_S3_CACHE = os.getenv('USE_S3_CACHE', True)