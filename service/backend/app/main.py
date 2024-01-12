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

app = FastAPI(
    title="Lighthouse",
    description="An open-source powerful activitypub relay written in Python!",
    version="0",
    contact={
        'name':"Mattholy",
        'url':"https://github.com/mattholy",
        'email':"smile.used@hotmail.com"
    },
    license_info= {
        "name": "MIT License",
        "url": "https://github.com/mattholy/lighthouse?tab=MIT-1-ov-file#readme",
    }
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
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"],
    response_class=JSONResponse
)
async def relay(request: Request, endpoint: str):
    return JSONResponse({'hello':'world','api':endpoint})

app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "web"), html=True), name="Lighthouse-Zero")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8080,reload=True)