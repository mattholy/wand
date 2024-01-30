# -*- encoding: utf-8 -*-
'''
main.py
----
put some words here


@Time    :   2024/01/12 14:02:23
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''
import os
import redis
from fastapi import FastAPI, Request, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from typing import Optional


from . import wand_env
from .setup import is_new_wand, get_wand_actor_and_wr
from .api.activitypub.relay import router as relay_router
from .model.wand_model import WandRelay, WandInit
from .model import activitypub_model
from .module_log import logger
from .utils.rsa import gen_key_pair
from .utils.activitypub_protocol import ActivityResponse


app = FastAPI(
    title="wand",
    description="An open-source powerful activitypub relay written in Python!",
    version=wand_env.VERSION,
    contact={
        'name': "Mattholy",
        'url': "https://github.com/mattholy",
        'email': "smile.used@hotmail.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/mattholy/wand?tab=MIT-1-ov-file#readme",
    },
    docs_url=None,
    redoc_url='/docs'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ProxyHeadersMiddleware)


@app.get('/init', tags=['Init'], name='Check Status of New Wand')
def init_status():
    if is_new_wand() is None:
        return JSONResponse({'new_wand': True})
    else:
        return JSONResponse({'new_wand': False})


@app.post(
    '/init',
    response_class=JSONResponse,
    tags=['Init'],
    name='Initialize New Wand'
)
def init(wand_init_item: WandInit):
    if is_new_wand() is None:
        logger.info('Initializing new wand ...')
        sec, pub = gen_key_pair()
        new_wand = WandRelay(
            actor_key_sec=sec, actor_key_pub=pub, **wand_init_item.model_dump())
        try:
            new_wand.save()
            logger.info('Wand is now up')
        except redis.exceptions.DataError as e:
            logger.critical(
                'Something went wrong when operating redis', exc_info=True)
            raise HTTPException(status_code=405, detail='request_body_unknown')
        from .model.wand_model import Base
        try:
            Base.metadata.create_all(wand_env.POSTGRES_POOL)
        except Exception as e:
            logger.critical(
                'Something went wrong when operating database', exc_info=True)
            raise HTTPException(status_code=501, detail='db_err')
        return JSONResponse(status_code=200, content={'wand_code': 0, 'wand_msg': 'ok', 'wand_data': None})
    else:
        logger.warn('Can not initialize again')
        raise HTTPException(
            status_code=405, detail='can_not_init_again')


app.include_router(relay_router)


@app.get("/.well-known/nodeinfo", response_class=JSONResponse, tags=['.well-known'], name='NodeinfoLinks', response_model=activitypub_model.NodeinfoLinks)
async def nodeinfolinks():
    return wand_env.NODE_INFO_LINKS


@app.get("/nodeinfo/2.1", response_class=JSONResponse, tags=['.well-known'], name='Nodeinfo', response_model=activitypub_model.Nodeinfo)
async def nodeinfo():
    res = wand_env.NODE_INFO
    res.usage.users.total = 1
    return res


@app.get("/actor", response_class=ActivityResponse, tags=['ActivityPub'], name='Actor', response_model=activitypub_model.Actor)
async def actor():
    logger.info('Incoming request for actor')
    actor, wr = get_wand_actor_and_wr()
    return ActivityResponse(content=actor.model_dump(by_alias=True))


@app.get("/.well-known/webfinger", response_class=ActivityResponse, tags=['.well-known'], name='Webfinger', response_model=activitypub_model.WebfingerResource)
async def read_webfinger(resource: Optional[str] = Query(None, pattern="acct:.+")):
    if resource is None:
        raise HTTPException(
            status_code=400, detail="Missing resource parameter")
    elif not resource.startswith('acct:wand@'):
        raise HTTPException(status_code=404)
    actor, wr = get_wand_actor_and_wr()
    res = activitypub_model.WebfingerResource(
        subject=resource,
        aliases=actor.id,
        links=[
            activitypub_model.WebfingerLink(
                rel='self',
                type='application/activity+json',
                href=actor.id
            ),
            activitypub_model.WebfingerLink(
                rel='self',
                type='application/ld+json; profile="https://www.w3.org/ns/activitystreams"',
                href=actor.id
            ),
        ]
    )

    return ActivityResponse(content=res.model_dump(by_alias=True))


@app.get("/.well-known/host-meta", tags=['.well-known'], name='Host-meta')
async def host_meta():
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
  <Link rel="lrdd" template="https://{wand_env.SERVER_URL}/.well-known/webfinger?resource={{uri}}"/>
</XRD>'''
    return Response(content=xml_content, media_type="application/xrd+xml; charset=utf-8")

app.mount("/",
          StaticFiles(
              directory=os.path.join(os.path.dirname(
                  os.path.abspath(__file__)), "web"),
              html=True
          ),
          name="wand-Zero"
          )
