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
from fastapi import Request
from fastapi import APIRouter

from utils.decode import decode_activity
from utils.activity import BaseActivity
from model import activitypub_model


router = APIRouter()


@router.api_route("/inbox", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
async def relay(activity:activitypub_model.Activity,request: Request):
    print(activity)
    activity = BaseActivity(request,activity)
    # print(dict(request.headers))
    # print(await decode_activity(request))
    return {"message": "Received"}
