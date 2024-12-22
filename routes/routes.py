from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.exceptions import CityDoesNotExist, WeatherDataSourceDoesNotExist
from adapters.dynamodb import write_log_to_dynamodb
from adapters.cdn_cache import CacheManager
from adapters.weather_api import WeatherDataManager
from utils.logging import get_logger
import settings

router = APIRouter()
logger = get_logger(__name__)


@router.get("/weather")
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
