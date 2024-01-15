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
import typing
from redis_om import HashModel
from pydantic import BaseModel

from ..wand_env import REDIS_POOL, SERVER_URL


class WandRelay(HashModel):
    actor_key: str = ''
    domain: str = SERVER_URL
    service_name: str
    service_desc: str
    service_icon: str
    service_image: str
    admin_gpg_public_key: str

    class Meta:
        database = redis.Redis(connection_pool=REDIS_POOL)


class WandInit(BaseModel):
    service_name: str
    service_desc: str
    service_icon: str
    service_image: str
    admin_gpg_public_key: str
