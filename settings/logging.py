import logging

import coloredlogs

def get_logger(module):
    logger = logging.getLogger('weather.api.' + module.split('.')[0])
    coloredlogs.install(level='DEBUG', logger=logger)
    return logger
