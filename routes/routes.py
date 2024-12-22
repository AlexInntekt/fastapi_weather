from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.exceptions import CityDoesNotExist, WeatherDataSourceDoesNotExist

from services.weather_service import WeatherService
from utils.logging import get_logger
import settings

router = APIRouter()
logger = get_logger(__name__)


@router.get("/weather") # TODO maybe integrate Pydantic
async def get_weather(city: str, data_source: str="openweathermap") -> JSONResponse:
    """
    Returns weather data for a specific city name.
    :param city: str
    :param data_source: str
        openweathermap is the Default
    :return:
    """

    try:
        weather_service = WeatherService(data_source)
        weather_data, found_cache, cache_file_path = await weather_service.get_weather(city)

        response = {
            'city': city,
            'weather': weather_data,
            'found_cache': True if found_cache else False,
            'file_path': cache_file_path
        }
        status_code = 200

    except (CityDoesNotExist, WeatherDataSourceDoesNotExist) as error:
        response = {
            'error': error.message
        }
        status_code = 404
        # TODO catch exceptions for provider API not responding, timeouts etc..

    finally:
        pass

    return JSONResponse(content=response, status_code=status_code)


@router.get('/cache')
async def get_cache(city: str ='Oradea') -> JSONResponse:
    """
    Return state of current cache for a city. You can use this for testing purposes.
    :param city: str
    :return:
    """
    response = await CacheManager().get_cache(city=city)

    return JSONResponse(content=response, status_code=200)
