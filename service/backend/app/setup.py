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
import logging

logger = logging.getLogger(__name__)

def setup() -> None:
    logger.info('Setting up your Wand...')
    check_environment_variables()

def check_environment_variables() -> None:
    required_vars = ['WD_SERVER_URL', 'WD_REDIS_SERVER', 'WD_REDIS_PORT','WD_POSTGRES_USER','WD_POSTGRES_PWD','WD_POSTGRES_SERVER','WD_POSTGRES_PORT','WD_POSTGRES_DBNAME']

    for var in required_vars:
        if var not in os.environ:
            logger.critical(f'Environment Variables not set: {var}')
            bye_bye = True
    if bye_bye:
        sys.exit(1)
