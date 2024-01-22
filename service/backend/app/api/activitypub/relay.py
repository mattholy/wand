# -*- encoding: utf-8 -*-
'''
inbox.py
----
handle relay api


@Time    :   2024/01/14 18:31:45
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import json
import requests
import hashlib
import base64
from urllib.parse import urlparse
from httpsig import HeaderVerifier
from fastapi import Request, APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from ...utils.activitypub_protocol import ActivityResponse, ActivityAction
from ...model import activitypub_model
from ...model import wand_model
from ...module_log import logger
from ... import wand_env
from ...setup import is_new_wand


router = APIRouter()


async def verify_actor(request: Request) -> dict:
    logger.debug(f'Incoming request with header: {request.headers}')
    body_raw = await request.body()
    body = json.loads(body_raw)
    try:
        logger.debug(f'Getting actor of activity')
        actor_res = requests.get(
            body['actor'],
            headers={
                'User-Agent': wand_env.USER_AGENT,
                'Accept': 'application/activity+json'
            }
        )
        actor_res = actor_res.json()
        actor = activitypub_model.Actor(**actor_res)
    except Exception as e:
        logger.warning(
            f'Can not fetch actor of activity'
        )
        logger.debug(e, exc_info=True)
        HTTPException(status_code=401)
    verifier = HeaderVerifier(
        headers=request.headers,
        required_headers=["(request-target)", "host",
                          "date", "digest", "content-type"],
        method=request.method,
        path=request.url.path,
        secret=actor.public_key.public_key_pem,
        sign_header='signature'
    )
    if not verifier.verify():
        logger.info(
            f'Can not verify requests from {actor.id}')
        raise HTTPException(status_code=401)

    logger.debug(f'Calculating the digest of origin')
    origin_digest = request.headers.get('digest')
    hash_obj = hashlib.sha256()
    hash_obj.update(body_raw)
    b = hash_obj.digest()
    calculated_digest = 'SHA-256=' + base64.b64encode(b).decode('utf-8')
    if origin_digest != calculated_digest:
        logger.warning(
            f'Can not verify digest of request from {actor.id}')
        raise HTTPException(status_code=401)

    logger.debug(f'All verifications pass')
    return actor


def react_to_activity(remoter_activity, remoter_actor) -> None:
    logger.debug(f'Begin to react to the activity from {remoter_actor.id}')
    act = ActivityAction(remoter_activity, remoter_actor)
    with wand_env.POSTGRES_SESSION() as s:
        r = wand_model.Activity(
            acivity_id=act.incoming_activity.id,
            server_uri=urlparse(act.incoming_actor.id).hostname,
            sender_uri=act.incoming_actor.id,
            data=act.incoming_activity.model_dump()
        )
        s.add(r)
        s.commit()


@router.post("/inbox", response_class=ActivityResponse, tags=['ActivityPub'], name='Inbox')
async def relay(
    react: BackgroundTasks,
    activity: activitypub_model.Activity,
    actor: dict = Depends(verify_actor)
):
    if 'https://www.w3.org/ns/activitystreams' not in activity.context:
        logger.warning(f'Remote activity with context: {activity.context}')
        raise HTTPException(
            detail='Only a "https://www.w3.org/ns/activitystreams" request can be send to this endpoint',
            status_code=401
        )
    if not isinstance(is_new_wand(), wand_model.WandRelay):
        logger.info('Can not process request before Wand is initiated')
        raise HTTPException(
            detail='Can not process your request before Wand is initiated',
            status_code=501
        )
    react.add_task(react_to_activity, activity, actor)
    return ActivityResponse(content=None, status_code=202)
