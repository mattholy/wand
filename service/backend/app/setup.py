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
from typing import Tuple

from .module_log import logger
from .model.wand_model import WandRelay
from .model import activitypub_model, wand_model
from .wand_env import REDIS_POOL, VERSION


def is_new_wand() -> WandRelay:
    try:
        res = WandRelay.all_pks()
    except redis.exceptions.ConnectionError as e:
        logger.critical('Can not connect to redis!')
        logger.debug(e, exc_info=True)
    res = [i for i in res]
    logger.debug(f'Get pks from redis are {res}')
    if res == []:
        return None
    target = WandRelay.get(res[0])
    logger.debug(f'The id about this wand are {target.wand_id}')
    if not target.wand_id:
        return None
    return target


def get_wand_actor_and_wr() -> Tuple[activitypub_model.Actor, wand_model.WandRelay]:
    wr = is_new_wand()
    wand_actor = activitypub_model.Actor(
        context=['https://www.w3.org/ns/activitystreams',
                 "https://w3id.org/security/v1"],
        id=f'https://{wr.service_domain}/actor',
        type='Application',
        name=wr.service_name,
        preferredUsername='wand',
        summary=wr.service_desc,
        inbox=f'https://{wr.service_domain}/actor/inbox',
        endpoints=activitypub_model.Endpoints(
            sharedInbox=f'https://{wr.service_domain}/inbox'),
        publicKey=activitypub_model.PublicKey(
            id=f'https://{wr.service_domain}/actor#main-key',
            owner=f'https://{wr.service_domain}/actor',
            publicKeyPem=wr.actor_key_sec
        ),
        icon=activitypub_model.Image(url=wr.service_icon),
        image=activitypub_model.Image(url=wr.service_image)
    )
    return wand_actor, wr
