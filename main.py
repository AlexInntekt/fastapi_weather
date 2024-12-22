import sys
import os
import time
import io



from fastapi import FastAPI
from fastapi.responses import JSONResponse

sys.path.append(os.getcwd())

import settings
from utils.logging import get_logger
from utils.exceptions import CityDoesNotExist, WeatherDataSourceDoesNotExist
from utils.dynamodb import write_log_to_dynamodb
from cdn_cache import CacheManager
from data_acquisition.weather import WeatherDataManager

app = FastAPI()
logger = get_logger(__name__)


@app.get("/weather")
async def get_weather(city: str, data_source: str="openweathermap") -> JSONResponse:
    """
    Returns weather data for a specific city name.
    :param city: str
    :param data_source: str
        openweathermap is the Default
    :return:
    """

    try:
        # Initialize variables
        file_path, result, found_cache = None, None, None


        if settings.USE_S3_CACHE:
            cache_manager = CacheManager()

            found_cache, file_path = await cache_manager.get_cache(city=city)

            if found_cache:
                logger.info(f"Retrieved cached data for city: {city} from S3. Cache Path: {file_path}")
                result = found_cache
            else:
                logger.info(f"Caching weather data for city: {city} into S3")
                weather_data_manager = WeatherDataManager.factory(data_source, city)
                result = await weather_data_manager.get_weather_data()

                file_path = await cache_manager.cache_to_s3(city, result)

        else:
            weather_data_manager = WeatherDataManager.factory(data_source, city)
            result = await weather_data_manager.get_weather_data()

        await write_log_to_dynamodb(city, file_path)

        response = {
            'city': city,
            'weather': result,
            'found_cache': True if found_cache else False,
            'file_path': file_path
        }
        status_code = 200

    except (CityDoesNotExist, WeatherDataSourceDoesNotExist) as error:
        response = {
            'error': error.message
        }
        status_code = 404

    finally:
        pass

    return JSONResponse(content=response, status_code=status_code)


# @app.get('/cache')
# async def get_cache(city: str ='Oradea') -> JSONResponse:
#     """
#     Return state of current cache.
#     :param city: str
#     :return:
#     """
#     response = CacheManager().get_cache(city=city)
#
#     return JSONResponse(content=response, status_code=200)
#
#
# @app.post('/cache')
# async def write_cache(city: str ='Oradea') -> JSONResponse:
#     """
#     Method to write a cache as test.
#     """
#
#     file_data = io.BytesIO(b"This is the content of the file.")
#
#     CacheManager().cache_to_s3(city, file_data)
#
#
# if __name__=='__main__':
#     print(f'Running main with settings: {settings.module_name}')