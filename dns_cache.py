import time

import boto3
from botocore.exceptions import NoCredentialsError

import settings
from utils.logging import get_logger


# Initialize S3 client
s3 = boto3.client('s3')
logger = get_logger(__name__)


class CacheManager():

    def __init__(self, bucket_name=settings.S3_BUCKET_NAME):
        self.bucket_name = bucket_name

    def cache_to_s3(self, city, data):
        bucket = settings.S3_BUCKET_NAME
        timestamp = str(time.time()).split('.')[0]
        file_key = city + f'/{timestamp}'

        s3.put_object(Bucket=self.bucket_name, Body=data, Key=file_key)
        logger.info(f"File '{file_key}' uploaded to S3 bucket '{bucket}' successfully.")

