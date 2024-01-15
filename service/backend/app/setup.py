# -*- encoding: utf-8 -*-
'''
setup.py
----
Init the wand


@Time    :   2024/01/14 17:59:44
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import sys
import os
import redis

from module_log import logger
from model.wand_model import WandRelay
from wand_env import REDIS_POOL


def setup() -> None:
    logger.info('Booting up your Wand...')
    check_environment_variables()
    logger.info('DONE')


def check_environment_variables() -> None:
    logger.info('Going to check environment variables')
    required_vars = ['WD_SERVER_URL', 'WD_REDIS_SERVER', 'WD_REDIS_PORT', 'WD_POSTGRES_USER',
                     'WD_POSTGRES_PWD', 'WD_POSTGRES_SERVER', 'WD_POSTGRES_PORT', 'WD_POSTGRES_DBNAME']

    for var in required_vars:
        if var not in os.environ:
            logger.critical(f'Environment Variables not set: {var}')
            bye_bye = True
    if bye_bye:
        sys.exit(1)
    logger.info('Environment variables are well-set')


def is_new_wand() -> bool:
    key_pattern = WandRelay.Meta.key_pattern()
    wand_redis = redis.Redis(REDIS_POOL)
    if wand_redis.exists(key_pattern):
        return False
    return True
