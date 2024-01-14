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


@app.api_route(
    '/api/{endpoint:path}',
    methods=["GET", "POST", "PUT", "DELETE",
             "OPTIONS", "HEAD", "PATCH", "TRACE"],
    response_class=JSONResponse,
    name='aaa',
    tags=['Other Services'], description='其它服务嵌入'
)
async def relay(request: Request, endpoint: str):
    return JSONResponse({'hello': 'world', 'api': endpoint})


@app.get("/.well-known/nodeinfo", response_class=JSONResponse, tags=['.well-known'], name='NodeinfoLinks',response_model=wand_env.NODE_INFO_LINKS)
async def nodeinfolinks():
    return wand_env.NODE_INFO_LINKS


@app.get("/nodeinfo/2.1", response_class=JSONResponse, tags=['.well-knownl'], name='Nodeinfo',response_model=wand_env.NODE_INFO)
async def nodeinfo():
    res = wand_env.NODE_INFO
    res.usage.users.total=1
    return res

app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "web"), html=True), name="wand-Zero")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8080, reload=True)
