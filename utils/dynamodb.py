import uuid
from datetime import datetime

import aioboto3

import settings


async def write_log_to_dynamodb(city: str, cdn_file_path: str):

    # Initialize an aioboto3 DynamoDB session
    async with aioboto3.Session().resource("dynamodb", region_name=settings.DYNAMODB_REGION_NAME) as dynamodb:
        # Get the table resource
        table = dynamodb.Table( settings.DYNAMODB_NAME )

        # Create a log entry
        log_entry = {
            "weather-access-log": str(uuid.uuid4()),
            "Timestamp": datetime.utcnow().isoformat(),  # Current timestamp
            "City": city, # City name
            "Cdn_file_path": cdn_file_path # Cdf file path
        }

        # Write the log to the table
        response = await table.put_item(Item=log_entry)
