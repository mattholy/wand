# -*- encoding: utf-8 -*-
'''
activity.py
----
handle activity


@Time    :   2024/01/15 14:37:41
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import requests
import json
from httpsig import HeaderVerifier
from fastapi import HTTPException, Request
from pydantic.error_wrappers import ValidationError

from model import activitypub_model
from module_log import logger


class BaseActivity:
    '''
    handle activity
    '''

    def __init__(self, incoming_req: Request, activity: activitypub_model.Activity) -> None:
        print(incoming_req.headers)
        try:
            self.request = incoming_req
            self.body = activity
        except ValidationError:
            raise HTTPException(status_code=401)
        self._verify_request_()

    def _verify_request_(self) -> bool:
        signature_parts = {}
        for part in self.request.headers.get('signature').split(","):
            key, value = part.strip().split("=", 1)
            key = key.strip('"')
            value = value.strip('"')
            signature_parts[key] = value
        try:
            logger.debug(f'Getting public key of {signature_parts["keyId"]}')
            res_of_key = requests.get(signature_parts['keyId'])
            res_of_key = res_of_key.json()
            self.pub_key = activitypub_model.PublicKey(
                **res_of_key['publicKey'])
        except:
            logger.warning(
                f'Can not retrieve public key of {signature_parts["keyId"]}')
        verifier = HeaderVerifier(
            headers=self.request.headers,
            required_headers=["(request-target)", "host",
                              "date", "digest", "content-type"],
            method=self.request.method,
            path=self.request.url.path,
            secret=self.pub_key.public_key_pem,
            sign_header='signature'
        )
        if not verifier.verify():
            logger.info(
                f'Can not verify requests from {signature_parts["keyId"]}')
            raise HTTPException(status_code=401)
