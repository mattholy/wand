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

import redis
import uuid
import hashlib
import base64
import datetime
import requests
from urllib.parse import urlparse
from typing import Tuple
from fastapi.responses import JSONResponse
from httpsig.requests_auth import HTTPSignatureAuth
from httpsig.sign import HeaderSigner

from .. import wand_env
from ..model import activitypub_model
from ..model import wand_model
from ..module_log import logger
from ..setup import get_wand_actor_and_wr


class ActivityAction:
    '''
    Actions as a activity response to remote
    '''

    def __init__(
        self,
        remoter_activity: activitypub_model.Activity,
        remoter_actor: activitypub_model.Actor
    ) -> None:
        self.incoming_activity = remoter_activity
        self.incoming_actor = remoter_actor
        self.actor, self.wr = get_wand_actor_and_wr()

        if self.incoming_activity.type == 'Follow':
            logger.info(
                f'Receiving Follow request from {self.incoming_activity.actor}'
            )
            if self.server_info_store():
                self.accept()
            else:
                self.deny()
        elif self.incoming_activity.type == 'Undo':
            logger.info(
                f'Receiving Undo request from {self.incoming_activity.actor}'
            )
            with wand_env.POSTGRES_SESSION() as s:
                r = s.query(wand_model.Subscriber).filter(wand_model.Subscriber.uri == urlparse(
                    self.incoming_actor.id).hostname).one_or_none()
                if r is None:
                    logger.warn(
                        f'No record found for {urlparse(self.incoming_actor.id).hostname}, ignore Undo request')
                else:
                    r.status = 'inactive'
                    s.commit()
        elif self.incoming_activity.type in [
            "Create",
            "Delete",
            "Follow",
            "Unfollow",
            "Like",
            "Announce",
            "Block",
            "Update",
            "Add",
            "Remove"
        ]:
            logger.info(
                f'Receiving {self.incoming_activity.type} request from {self.incoming_activity.actor}'
            )
            # broadcast
        else:
            logger.error(
                f'Received request from {self.incoming_activity.actor} with type {self.incoming_activity.type}, not handled. Raw body is {self.incoming_activity}'
            )

    def server_info_store(self) -> bool:
        logger.debug(f'Fetch remote service info')
        incoming_uri = urlparse(self.incoming_actor.id)
        hostname = incoming_uri.hostname
        with wand_env.POSTGRES_SESSION() as s:
            r = s.query(wand_model.Subscriber).filter(
                wand_model.Subscriber.server_id == hostname).one_or_none()
        if r is not None:
            return r.status != 'block'
        logger.info(f'New instance request to follow: {hostname}')
        scheme = incoming_uri.scheme
        try:
            instance = requests.get(
                f'{scheme}://{hostname}/api/v1/instance').json()
            nodeinfo = requests.get(
                f'{scheme}://{hostname}/.well-known/nodeinfo').json()
            nodeinfo = requests.get(nodeinfo['links'][0]['href']).json()
        except Exception as e:
            logger.warn(
                f'Something went wrong when fetch info about {hostname}')
            logger.debug(e, exc_info=True)
            return False
        r = wand_model.Subscriber(
            server_id=hostname,
            name=instance['title'],
            desc=instance['short_description'],
            icon=instance['thumbnail'],
            status='active',
            instance=instance,
            nodeinfo=nodeinfo,
        )
        with wand_env.POSTGRES_SESSION() as s:
            s.add(r)
            s.commit()
        return True

    def sign(self, msg: activitypub_model.Activity) -> Tuple[str, dict, HTTPSignatureAuth]:
        body = msg.model_dump_json(by_alias=True)
        digest = base64.b64encode(hashlib.sha256(
            body.encode()).digest()).decode()
        headers = {
            'Content-Type': 'application/activity+json',
            'Accept': 'application/activity+json',
            'Content-Length': str(len(body)),
            'User-Agent': wand_env.USER_AGENT,
            'Digest': f'SHA-256={digest}',
            'Host': urlparse(self.incoming_activity.actor).netloc,
            'Date': datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            'Connection': 'keep-alive'
        }
        headers_to_sign = ["(request-target)", "host",
                           "date", "digest", "content-type"]
        signer = HeaderSigner(
            key_id=self.actor.public_key.id,
            secret=self.actor.public_key.public_key_pem,
            algorithm="rsa-sha256",
            headers=headers_to_sign
        )
        signed_headers = signer.sign(
            headers, method="post",
            path=urlparse(self.incoming_actor.endpoints.shared_inbox).path
        )
        headers['Signature'] = signed_headers['Authorization'][len(
            "Signature "):]
        return body, headers

    def send_msg(self, msg: activitypub_model.Activity) -> None:
        body, headers = self.sign(msg)
        logger.debug(f'Sending request to remote actor with body: {body}')
        response = requests.post(
            self.incoming_actor.endpoints.shared_inbox,
            data=body,
            headers=headers
        )
        logger.debug(
            f'Response code from remote is {response.status_code} with body: {response.text}')

    def accept(self) -> bool:
        logger.debug(
            f'Accepting new {self.incoming_activity.type} request from {self.incoming_activity.actor}')
        react_accept = activitypub_model.Activity(
            context='https://www.w3.org/ns/activitystreams',
            type='Accept',
            to=[self.incoming_actor.id],
            id=f'https://{wand_env.SERVER_URL}/activities/{uuid.uuid4()}',
            actor=self.actor.id,
            object=self.incoming_activity
        )
        self.send_msg(react_accept)

    def deny(self) -> bool:
        pass

    def undo(self) -> bool:
        pass


class ActivityResponse(JSONResponse):
    media_type = "application/activity+json"
