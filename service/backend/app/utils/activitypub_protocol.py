# -*- encoding: utf-8 -*-
'''
activitypub_protocol.py
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
import hashlib
import base64
from httpsig import HeaderVerifier
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

import wand_env
from model import activitypub_model
from module_log import logger


class ActivityEntity:
    '''
    handle activity
    '''

    def __init__(self, incoming_req: Request, body: bytes) -> None:
        self.request = incoming_req
        self.body = body
        self._verify_request_()
        self._verify_digest_()
        try:
            self.activity = activitypub_model.Activity(
                **(json.loads(body.decode()))
            )
        except ValidationError:
            raise HTTPException(status_code=401)
        self._fetch_remote_actor_()

    def _verify_request_(self) -> bool:
        signature_parts = {}
        for part in self.request.headers.get('signature').split(","):
            key, value = part.strip().split("=", 1)
            key = key.strip('"')
            value = value.strip('"')
            signature_parts[key] = value
        try:
            logger.debug(f'Getting public key of {signature_parts["keyId"]}')
            res_of_key = requests.get(
                signature_parts['keyId'],
                headers={
                    'User-Agent': wand_env.USER_AGENT,
                    'Accept': 'application/activity+json'
                }
            )
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

    def _verify_digest_(self):
        logger.debug(f'Calculating the digest of origin')
        origin_digest = self.request.headers.get('digest')
        hash_obj = hashlib.sha256()
        hash_obj.update(self.body)
        b = hash_obj.digest()
        calculated_digest = 'SHA-256=' + base64.b64encode(b).decode('utf-8')
        if origin_digest != calculated_digest:
            logger.warning(
                f'Can not verify digest of request from {json.loads(self.body.decode())["id"]}')
            raise HTTPException(status_code=401)

    def _fetch_remote_actor_(self):
        logger.debug(
            f'Fetching remote actor of {json.loads(self.body.decode())["id"]}')
        try:
            remote_actor = requests.get(
                self.activity.actor,
                headers={
                    'User-Agent': wand_env.USER_AGENT,
                    'Accept': 'application/activity+json'
                }
            )
            assert remote_actor.status_code == 200, remote_actor.status_code
            try:
                self.remote_actor = activitypub_model.Actor(
                    **remote_actor.json())
                return
            except ValidationError:
                logger.error(
                    f'Unparsable data from remote actor of {json.loads(self.body.decode())["id"]}', remote_actor.json())
        except AssertionError:
            logger.warn(
                f'Can not fetching remote actor of {json.loads(self.body.decode())["id"]}, because of a status code: {remote_actor.status_code}')
        except:
            logger.error(
                f'Something wrong when fetching remote actor of {json.loads(self.body.decode())["id"]}', exc_info=True)
        raise HTTPException(status_code=401)


class ActivityResponse(JSONResponse):
    media_type = "application/activity+json"
