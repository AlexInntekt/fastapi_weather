import os
import importlib

from .logging import get_logger

env = os.environ.get('ENV', 'local')  # Default to 'local' if ENV is not set
module_name = f"settings.{env}"
logger = get_logger(__name__)


try:
    settings_module = importlib.import_module(module_name)
    globals().update(vars(settings_module))
    logger.info(f'RUNNING APPLICATION WITH MODULE SETTINGS: {module_name}')
except ModuleNotFoundError:
    raise ImportError(f"Settings module '{module_name}' not found. Check your ENV variable.")
