import os

CACHE_TTL = os.getenv('CACHE_TTL', 5)
USE_S3_CACHE = os.getenv('USE_S3_CACHE', True)
DELETE_ALL_CACHED_FILES = os.getenv('DELETE_ALL_CACHED_FILES', True)
S3_REGION_NAME = os.getenv('S3_REGION_NAME', 'eu-central-1')
DYNAMODB_REGION_NAME = os.getenv('DYNAMODB_REGION_NAME', 'eu-central-1')
DYNAMODB_NAME = os.getenv('DYNAMODB_NAME', 'TempDynamoDB')