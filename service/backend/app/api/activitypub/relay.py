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

from fastapi import Request
from fastapi import APIRouter

from .utils.decode import decode_activity

router = APIRouter()


@router.api_route("/inbox", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
async def relay(request: Request):
    print(dict(request.headers))
    print(await decode_activity(request))
    return {"message": "Received"}
