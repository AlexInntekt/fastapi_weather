from adapters.dynamodb import write_log_to_dynamodb
from adapters.cdn_cache import CacheManager
from adapters.weather_api import WeatherSourceManager
import settings
import logging

logger = logging.getLogger(__name__)


class WeatherService():

    def __init__(self, data_source: str):
        self.data_source = data_source


    async def get_weather(self, city):
        file_path, weather_data, found_cache = None, None, None

        if settings.USE_S3_CACHE:
            cache_manager = CacheManager()

            found_cache, file_path = await cache_manager.get_cache(city=city)

            if found_cache:
                logger.info(f"Retrieved cached data for city: {city} from S3. Cache Path: {file_path}")
                weather_data = found_cache
            else:
                logger.info(f"Caching weather data for city: {city} into S3")
                weather_data_manager = WeatherSourceManager.factory(self.data_source, city)
                weather_data = await weather_data_manager.get_weather_data()

                file_path = await cache_manager.cache_to_s3(city, weather_data)

        else:
            weather_data_manager = WeatherSourceManager.factory(self.data_source, city)
            weather_data = await weather_data_manager.get_weather_data()

        await write_log_to_dynamodb(city, file_path)

        return weather_data, found_cache, file_path