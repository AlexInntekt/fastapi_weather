

class CityDoesNotExist(Exception):
    """Exception raised for city name input"""

    def __init__(self, city_name, message="City name does not exist:"):
        self.city_name = city_name
        self.message = message + f' {city_name}'
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} You entered: {self.city_name}"