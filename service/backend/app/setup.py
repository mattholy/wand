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

from .module_log import logger
from .model.wand_model import WandRelay
from .wand_env import REDIS_POOL, VERSION


def is_new_wand() -> bool:
    key_pattern = "WandRelay:*"
    wand_redis = redis.Redis(connection_pool=REDIS_POOL)
    if wand_redis.keys(key_pattern):
        return False
    return True
