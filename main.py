import sys
import os

import requests
import aiohttp

from fastapi import FastAPI
from fastapi.responses import JSONResponse

sys.path.append(os.getcwd())

import settings
from utils.logging import get_logger
from utils.exceptions import CityDoesNotExist

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
        result = await WeatherDataManager(city).get_weather_data()

        response = {
            'city': city,
            'weather': result
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



if __name__=='__main__':
    print(f'Running main with settings: {settings.module_name}')