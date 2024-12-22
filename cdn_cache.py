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
    """
    Cache manager class that deals with operations on the S3 bucket for cache retrieval, creation and deletion.
    """

    def __init__(self, bucket_name=settings.S3_BUCKET_NAME):
        self.bucket_name = bucket_name

    async def cache_to_s3(self, city, data):
        """
        Procedure to cache the data for a specific city. It will upload the cached data to S3 as a file.
        :param city: str
        :param data: str
        :return:
        """
        bucket = settings.S3_BUCKET_NAME
        timestamp = str(time.time()).split('.')[0]
        file_key = city + f'/{city}_{timestamp}.json' # Example: London/Longon_1734772959
        data = json.dumps(data).encode('utf-8') # we need to have the data in bytes format

        if settings.DELETE_ALL_CACHED_FILES: # set to False in case you want to save previous file states
            await self.delete_city_cached_files(city)

        # upload to s3 CDN:
        async with aioboto3.client('s3', region_name=settings.S3_REGION_NAME) as s3_client:
            await s3_client.put_object(Bucket=self.bucket_name, Body=data, Key=file_key)
        logger.info(f"File '{file_key}' uploaded to S3 bucket '{bucket}' successfully.")

        return file_key


    async def delete_city_cached_files(self, city):
        """
        Cleanup procedure that deletes all cached files for a specific city name.
        :param city: str
        :return:
        """
        prefix = f"{city}/"

        async with aioboto3.client('s3', region_name=settings.S3_REGION_NAME) as s3_client:
            # list all cached files under the 'city/' key
            response = await s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)

            if 'Contents' in response:
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

                await s3_client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})
                logger.info(f"Deleted files in directory '{prefix}' from bucket '{self.bucket_name}'.")


    async def get_cached_objects_for_city(self, city: str):
        """
        Returns a list of cache file names for a specific city.
        :param city: str
        :return:
        """
        async with aioboto3.client('s3', region_name=settings.S3_REGION_NAME) as s3_client:
            s3_directory = await s3_client.list_objects(Bucket=self.bucket_name, Prefix=city)
            result = s3_directory.get('Contents')

        return result



    async def download_file(self, object_key):
        """
        Downloads the content of cached file
        :param object_key: str
            The file path. Example: Cluj_1734771596.json
        :return:
        """
        async with aioboto3.client('s3', region_name=settings.S3_REGION_NAME) as s3_client:
            response = await s3_client.get_object(Bucket=self.bucket_name, Key=object_key)

            async with response['Body'] as stream:
                content = await stream.read()
                return content.decode('utf-8')


    async def get_cache(self, city):
        """
        Get cached data for city. It will make a download on S3 to get the content of the cached file.
        :param city: str
            The city name. Example: Cluj
        :return: JSON
        """
        current_time = datetime.now(timezone.utc)
        last_n_minutes = current_time - timedelta(minutes=settings.CACHE_TTL)

        # get all cached files for this city
        files = await self.get_cached_objects_for_city(city)
        if files:
            files = [file for file in files if file['LastModified'] >= last_n_minutes]

        file_content = None
        file_path = None
        file = None

        # if there exists at least one file, start downloading its content
        if files:
            file = files[0]
            file_path = file['Key']

        if file:
            file_content = await self.download_file(file['Key'])
            file_content = json.loads(file_content)


        return file_content, file_path