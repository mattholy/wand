# -*- encoding: utf-8 -*-
'''
wand_model.py
----
Data model of wand system


@Time    :   2024/01/15 19:09:25
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import redis
from redis_om import HashModel

from wand_env import REDIS_POOL


class WandRelay(HashModel):
    name: str
    price: float
    in_stock: int

    class Meta:
        database = redis.Redis(connection_pool=REDIS_POOL)
