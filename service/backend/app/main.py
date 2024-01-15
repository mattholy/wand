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
from starlette.responses import Response
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import wand_env
from setup import setup, is_new_wand
from api.activitypub.relay import router as relay_router
from model.wand_model import WandRelay


setup()

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

if is_new_wand():
    from model.wand_model import WandInit

    @app.post(
        '/init',
        response_class=JSONResponse,
        tags=['Init'],
        name='Initiate New Wand'
    )
    def init(wand_init_item: WandInit):
        new_wand = WandRelay(**WandInit)
        new_wand.save()
        return JSONResponse(status_code=200, content={})


app.include_router(relay_router)


@app.get("/.well-known/nodeinfo", response_class=JSONResponse, tags=['.well-known'], name='NodeinfoLinks', response_model=wand_env.NODE_INFO_LINKS)
async def nodeinfolinks():
    return wand_env.NODE_INFO_LINKS


@app.get("/nodeinfo/2.1", response_class=JSONResponse, tags=['.well-known'], name='Nodeinfo', response_model=wand_env.NODE_INFO)
async def nodeinfo():
    res = wand_env.NODE_INFO
    res.usage.users.total = 1
    return res

app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "web"), html=True), name="wand-Zero")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8080, reload=True)
