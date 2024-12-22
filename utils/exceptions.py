
class WeatherDataSourceDoesNotExist(Exception):
    """Exception raised when a weather data source is mentioned but it does not exist"""

    def __init__(self, data_source_name, message="Weather data source does not exist:"):
        self.data_source_name = data_source_name
        self.message = message + f' {data_source_name}'
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} You entered: {self.data_source_name}"


class CityDoesNotExist(Exception):
    """Exception raised for city name that does not exist."""

    def __init__(self, city_name, message="City name does not exist:"):
        self.city_name = city_name
        self.message = message + f' {city_name}'
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} You entered: {self.city_name}"