import time
import json
from datetime import datetime, timezone, timedelta

import boto3
import aioboto3
from botocore.exceptions import NoCredentialsError

import settings
from utils.logging import get_logger


# Initialize S3 client

logger = get_logger(__name__)


class CacheManager():

    def __init__(self, bucket_name=settings.S3_BUCKET_NAME):
        self.bucket_name = bucket_name

    async def cache_to_s3(self, city, data):
        bucket = settings.S3_BUCKET_NAME
        timestamp = str(time.time()).split('.')[0]
        file_key = city + f'/{city}_{timestamp}.json'
        data = json.dumps(data).encode('utf-8')

        if settings.DELETE_ALL_CACHED_FILES:
            await self.delete_city_cached_files(city)

        async with aioboto3.client('s3') as s3_client:
            await s3_client.put_object(Bucket=self.bucket_name, Body=data, Key=file_key)
        logger.info(f"File '{file_key}' uploaded to S3 bucket '{bucket}' successfully.")


    async def delete_city_cached_files(self, city):
        prefix = f"{city}/"

        async with aioboto3.client('s3') as s3_client:
            response = await s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)

            if 'Contents' in response:
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

                await s3_client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})
                logger.info(f"Deleted files in directory '{prefix}' from bucket '{self.bucket_name}'.")


    async def get_cached_objects_for_city(self, city: str):
        async with aioboto3.client('s3') as s3_client:
            s3_directory = await s3_client.list_objects(Bucket=self.bucket_name, Prefix=city)
            result = s3_directory.get('Contents')

        return result



    async def download_file(self, object_key):
        async with aioboto3.client('s3') as s3_client:
            response = await s3_client.get_object(Bucket=self.bucket_name, Key=object_key)

            # Read the body of the response
            async with response['Body'] as stream:
                content = await stream.read()
                return content.decode('utf-8')  # Decode bytes to string (if the file is text-based)


    async def get_cache(self, city):
        current_time = datetime.now(timezone.utc)
        last_n_minutes = current_time - timedelta(minutes=settings.CACHE_TTL)

        files = await self.get_cached_objects_for_city(city)
        if files:
            files = [file for file in files if file['LastModified'] >= last_n_minutes]

        file_content = None
        file_timestamp = None
        file = None

        if files:
            file = files[0]
            print(file)
            file_timestamp = file['Key']

        if file:
            file_content = await self.download_file(file['Key'])
            file_content = json.loads(file_content)


        return file_content, file_timestamp