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
import uuid
from redis_om import HashModel, Field
from pydantic import BaseModel

from ..wand_env import REDIS_POOL, SERVER_URL


class WandRelay(HashModel):
    wand_id: str = str(uuid.uuid4())
    actor_key_sec: str
    actor_key_pub: str
    service_domain: str = SERVER_URL
    service_name: str
    service_desc: str
    service_icon: str = ""
    service_image: str = ""
    admin_gpg_public_key: str
    agreements: str = 'False'

    class Meta:
        database = redis.Redis(connection_pool=REDIS_POOL)


class WandInit(BaseModel):
    service_name: str
    service_desc: str
    admin_gpg_public_key: str
    agreements: bool
