from .base import *

import os

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_KEY')
OPENWEATHERMAP_BASE_URL = os.getenv('OPENWEATHERMAP_BASE_URL')

if not OPENWEATHERMAP_API_KEY:
    raise ValueError("The OPENWEATHERMAP_API_KEY setting is not configured.")

if not OPENWEATHERMAP_BASE_URL:
    raise ValueError("The OPENWEATHERMAP_BASE_URL setting is not configured.")
