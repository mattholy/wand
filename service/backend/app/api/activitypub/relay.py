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
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse

from ...utils.decode import decode_activity
from ...utils.activitypub_protocol import ActivityEntity, ActivityResponse
from ...model import activitypub_model
from ...module_log import logger


router = APIRouter()


@router.post("/inbox", response_class=ActivityResponse)
async def relay(request: Request):
    body = await request.body()
    incoming_request = ActivityEntity(request, body)
    return ActivityResponse(content=None, status_code=202)
