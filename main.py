import requests
import aiohttp

from fastapi import FastAPI

from weather import settings


app = FastAPI()




async def get_openweathermap_data(url, city):
    url = url + f'?appid={config.OPENWEATHERMAP_API_KEY}' + f'&q={city}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = (await response.json()).get('fact')
            return data

async def get_data(city):
    return await get_openweathermap_data(config.OPENWEATHERMAP_BASE_URL, city)


@app.get("/weather")
async def weather(city):

    result = await get_data(None)

    response = {
        'city': city,
        'weather': result
    }
    return response

if __name__=='__main__':
    print(f'Running main with settings: {settings.module_name}')