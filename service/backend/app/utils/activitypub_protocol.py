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
import asyncio
import aiohttp
import certifi
import ssl
import arrow
from urllib.parse import urlparse
from typing import Tuple, Type, Optional
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

    @classmethod
    def parse(
        cls: Type['ActivityAction'],
        remoter_activity: activitypub_model.Activity,
        remoter_actor: activitypub_model.Actor
    ) -> 'ActivityAction':
        action = cls(remoter_activity, remoter_actor)
        action.process_activity()
        return action

    def process_activity(self) -> None:
        if self.incoming_activity.type == 'Follow':
            logger.info(
                f'Receiving Follow request from {self.incoming_activity.actor}'
            )
            if self.check_server_is_ok():
                self.accept()
            else:
                self.deny()
        elif self.incoming_activity.type == 'Undo':
            logger.info(
                f'Receiving Undo request from {self.incoming_activity.actor}'
            )
            with wand_env.POSTGRES_SESSION() as s:
                r = s.query(wand_model.Subscriber).filter(
                    wand_model.Subscriber.server_id == urlparse(
                        self.incoming_actor.id).hostname
                ).one_or_none()
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
            asyncio.run(self.broadcast())
        else:
            logger.error(
                f'Received request from {self.incoming_activity.actor} with type {self.incoming_activity.type}, not handled. Raw body is {self.incoming_activity}'
            )

    def check_server_is_ok(self) -> bool:
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
            inbox=self.incoming_actor.endpoints.shared_inbox,
            software=nodeinfo['software']['name'],
            subscription_return_msg='',
            status='pending',
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

    async def send_msg(
        self,
        msg: activitypub_model.Activity,
        destination: str
    ) -> aiohttp.ClientResponse:
        body, headers = self.sign(msg)
        logger.debug(f'Sending request to {destination} with body: {body}')
        hostname = urlparse(destination).hostname
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                async with session.post(destination, data=body, headers=headers) as resp:
                    response = resp
                    response_text = await resp.text()
                    logger.debug(
                        f'Response code from {hostname} is {resp.status} with body: {response_text}')
                    try:
                        async with wand_env.POSTGRES_SESSION_ASYNC() as s:
                            broadcast_record = wand_model.BroadcastRecord(
                                activity_id=msg.id,
                                destnation_server_id=hostname,
                                status='SUCCESS' if response.status in [
                                    200, 202] else 'FAILURE',
                            )
                            logger.debug(
                                f'Save response from {hostname} to database')
                            s.add(broadcast_record)
                            await s.commit()
                    except Exception as db_error:
                        logger.error(
                            f'Error when saving broadcast record to database: {db_error}')
                    finally:
                        return response, response_text
            except Exception as e:
                logger.error(
                    f'Error when sending data to {hostname}')
                logger.debug(e, exc_info=True)
                try:
                    async with wand_env.POSTGRES_SESSION_ASYNC() as s:
                        broadcast_record = wand_model.BroadcastRecord(
                            activity_id=msg.id,
                            destnation_server_id=hostname,
                            status='FAILURE',
                        )
                        logger.debug(
                            f'Save response from {hostname} to database')
                        s.add(broadcast_record)
                        await s.commit()
                except Exception as db_error:
                    logger.error(
                        f'Error when saving broadcast record to database: {db_error}')
                raise e

    def accept(self) -> bool:
        logger.debug(
            f'Accepting new {self.incoming_activity.type} request from {self.incoming_activity.actor}')
        incoming_uri = urlparse(self.incoming_actor.id)
        hostname = incoming_uri.hostname
        with wand_env.POSTGRES_SESSION() as s:
            loaded_r = s.query(wand_model.Subscriber).filter_by(
                server_id=hostname).one_or_none()
            if loaded_r is None:
                logger.error(f'Tring to accept unknown server')
                return False
            loaded_r.status = 'waiting'
            react_accept = activitypub_model.Activity(
                context='https://www.w3.org/ns/activitystreams',
                type='Accept',
                to=[self.incoming_actor.id],
                id=f'https://{wand_env.SERVER_URL}/activities/{uuid.uuid4()}',
                actor=self.actor.id,
                object=self.incoming_activity
            )
            wand_activity_for_save = wand_model.Activity(
                activity_id=react_accept.id,
                server_id=self.wr.service_domain,
                sender_id=self.actor.id,
                data=react_accept.model_dump(by_alias=True)
            )
            s.add(wand_activity_for_save)
            try:
                res, response_text = asyncio.run(
                    self.send_msg(
                        react_accept,
                        self.incoming_actor.endpoints.shared_inbox
                    )
                )
                assert res.status == 200 or res.status == 202
                loaded_r.status = 'active'
                loaded_r.subscription_return_msg = response_text
            except AssertionError:
                logger.warn(
                    f'Error when send Accept Object to {self.incoming_actor.id}. Response body is {res.text}')
                loaded_r.subscription_return_msg = response_text
                return False
            except Exception as e:
                logger.error(
                    f'Error when send Accept Object to {self.incoming_actor.id} with exception 「{e}」')
                logger.debug(e, exc_info=True)
                return False
            finally:
                s.commit()
            logger.info(
                f'Done with accepting Follow request from {self.incoming_actor.id}')
            return True

    def deny(self) -> bool:
        pass

    def undo(self) -> bool:
        pass

    async def broadcast(self) -> bool:
        payload = activitypub_model.Activity(
            context='https://www.w3.org/ns/activitystreams',
            id=f'https://{self.wr.service_domain}/activities/{uuid.uuid4()}',
            type='Announce',
            actor=self.actor.id,
            object=self.incoming_activity.id,
            to=[f"https://{self.wr.service_domain}/actor/followers"]
        )
        broadcast_activity = wand_model.Activity(
            activity_id=payload.id,
            server_id=self.wr.service_domain,
            sender_id=self.actor.id,
            data=payload.model_dump(by_alias=True)
        )
        with wand_env.POSTGRES_SESSION() as s:
            s.add(broadcast_activity)
            s.commit()
            subscribers = s.query(wand_model.Subscriber).filter(
                wand_model.Subscriber.status == 'active').all()
        if not subscribers:
            logger.info(
                'No active subscribers found. Incoming activity will not be broadcasted')
            return False
        tasks = []
        start_time = arrow.now()
        for subscriber in subscribers:
            task = asyncio.create_task(
                self.send_msg(payload, subscriber.inbox)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = arrow.now()
        last = (end_time - start_time).seconds
        s = 0
        f = 0
        for r in responses:
            if isinstance(r, Exception):
                f = f + 1
            else:
                s = s + 1
        logger.info(
            f'Finish broadcast in {last}s, to {len(responses)} subscribers, {f} failures, {s} successes.')

        return True


class ActivityResponse(JSONResponse):
    media_type = "application/activity+json"
