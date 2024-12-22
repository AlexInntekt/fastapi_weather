import sys
import os
import time
import io

import requests
import aiohttp

from fastapi import FastAPI
from fastapi.responses import JSONResponse

sys.path.append(os.getcwd())

import settings
from utils.logging import get_logger
from utils.exceptions import CityDoesNotExist
from utils.dynamodb import write_log_to_dynamodb
from cdn_cache import CacheManager

app = FastAPI()
logger = get_logger(__name__)



class WeatherDataManager():
    def __init__(self, city: str):
        self.city = city


    async def get_openweathermap_data(self, url: str):
        city = self.city

        url = url + f'?appid={settings.OPENWEATHERMAP_API_KEY}' + f'&q={city}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_code = response.status

                if status_code == 404:
                    # TODO find a way to figure out for sure if the 404 is caused by a wrong city name.
                    #  404 can be caused by a change in the root URL made by the weather data provider
                    logger.debug(f'A request was made for a city that does not exist {city}')
                    raise CityDoesNotExist(city)

                data = (await response.json())
                return data


    async def get_weather_data(self):
        return await self.get_openweathermap_data(settings.OPENWEATHERMAP_BASE_URL)


@app.get("/weather")
async def get_weather(city: str) -> JSONResponse:
    """
    Returns weather data for a specific city name.
    :param city: str
    :return:
    """

    try:
        if settings.USE_S3_CACHE:
            found_cache, file_path = await CacheManager().get_cache(city=city)

            if found_cache is None:
                logger.info(f'CACHING WEATHER DATA FOR CITY {city} INTO S3')

                result = await WeatherDataManager(city).get_weather_data()
                file_path = await CacheManager().cache_to_s3(city, result)
            else:
                logger.info(f'CACHED DATA FOR CITY {city} WAS FOUND. {found_cache}')
                result = found_cache

        else:
            result = await WeatherDataManager(city).get_weather_data()
            file_path = None

        await write_log_to_dynamodb(city, file_path)

        response = {
            'city': city,
            'weather': result,
            'found_cache': True if found_cache else False,
            'file_path': file_path
        }
        status_code = 200

    except CityDoesNotExist as error:
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