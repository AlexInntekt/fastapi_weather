
import requests
import aiohttp

from abc import ABC, abstractmethod

from utils.logging import get_logger
import settings

logger = get_logger(__name__)


class WeatherDataManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def get_weather_data(self):
        pass


class OpenWeatherMapDataManager(WeatherDataManager):
    def __init__(self, city: str):
        self.city = city
        super().__init__()


    async def get_weather_data(self):
        city = self.city
        url = settings.OPENWEATHERMAP_BASE_URL

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
