import requests
import aiohttp

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from weather import settings
from weather.utils.logging import get_logger
from weather.utils.exceptions import CityDoesNotExist

app = FastAPI()
logger = get_logger(__name__)



async def get_openweathermap_data(url, city):
    url = url + f'?appid={settings.OPENWEATHERMAP_API_KEY}' + f'&q={city}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status_code = response.status

            if status_code == 404:
                logger.debug(f'A request was made for a city that does not exist {city}')
                raise CityDoesNotExist(city)

            data = (await response.json())
            return data

async def get_weather_data(city):
    return await get_openweathermap_data(settings.OPENWEATHERMAP_BASE_URL, city)


@app.get("/weather")
async def weather(city):

    try:
        result = await get_weather_data(city)

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