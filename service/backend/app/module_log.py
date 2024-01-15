# -*- encoding: utf-8 -*-
'''
module_log.py
----
logging


@Time    :   2024/01/14 22:34:35
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''


import logging
from colorlog import ColoredFormatter

from .wand_env import VERSION


logger = logging.getLogger()
logger.setLevel(logging.DEBUG if VERSION == 'DEV' else logging.INFO)


handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(asctime)s - %(log_color)s%(levelname)s%(reset)s - [%(filename)s:%(lineno)d] : "
    "%(message_log_color)s%(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'bold_red',
        'CRITICAL': 'bold_red',
    },
    secondary_log_colors={
        'message': {
            'CRITICAL': 'bold'
        }
    },
    style='%'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
