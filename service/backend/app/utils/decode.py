# -*- encoding: utf-8 -*-
'''
decode.py
----
decode activitypub's activity


@Time    :   2024/01/14 19:41:30
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import hashlib
import base64
import json
import requests
import logging
from fastapi import Request, HTTPException
from typing import Optional
from httpsig import HeaderVerifier

from model import activitypub_model

logger = logging.getLogger('')
async def decode_activity(request: Request) -> (activitypub_model.Activity, activitypub_model.Actor,bytes):
    body = await request.body()
    # Verify HTTP Signature
    print(body)
    signature_parts = {}
    for part in request.headers.get('signature').split(","):
        key, value = part.strip().split("=", 1)
        key = key.strip('"')
        value = value.strip('"')
        signature_parts[key] = value
    try:
        res_of_key = requests.get(signature_parts['keyId'])
        res_of_key = res_of_key.json()
        pub_key = res_of_key['publicKey']['publicKeyPem']
    except Exception as e:
        pass
    print(pub_key)
    verifier = HeaderVerifier(
        headers=request.headers,
        required_headers=["(request-target)","host", "date", "digest", "content-type"],
        method=request.method,
        path=request.url.path,
        secret=pub_key,
        sign_header='signature'
    )
    if not verifier.verify():
        print("签名验证成功！")
    else:
        print("签名验证失败！")
    # Verify Digest
    given_digest = request.headers.get("Digest")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(body)
    calculated_digest = "SHA-256=" + base64.b64encode(sha256_hash.digest()).decode()

    if given_digest != calculated_digest:
        raise HTTPException(status_code=400, detail="Digest mismatch")
    
    # Parse Activity
    try:
        activity = json.loads(body, cls=activitypub_model.Activity)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return activity, '', body

