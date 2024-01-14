# -*- encoding: utf-8 -*-
'''
env.py
----
setup some env 


@Time    :   2024/01/12 18:09:40
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import os
import sqlalchemy
import redis
from sqlalchemy import create_engine

from model import activitypub_model

# Env
VERSION = os.environ.get('WD_VERSION', 'DEV')
SERVER_URL = os.environ.get('WD_SERVER_URL', 'localhost')
ADMIN_PUB_KEY = os.environ.get('WD_ADMIN_PGP_PUB_KEYFILE', 'localhost')

# Base Info
NODE_INFO_LINKS = activitypub_model.NodeInfoLinks(links=[
    activitypub_model.Link(
        rel="http://nodeinfo.diaspora.software/ns/schema/2.1",
        href=f"https://{SERVER_URL}/nodeinfo/2.1"
    )
])
NODE_INFO = activitypub_model.NodeInfoModel(
    version="2.1",
    software=activitypub_model.Software(
        name="wand",
        version=VERSION,
        repository="https://github.com/mattholy/wand"
    ),
    protocols=["activitypub"],
    services={"inbound": [], "outbound": []},
    openRegistrations=True,
    usage=activitypub_model.Usage(
        users=activitypub_model.Users(
            total=0,
            activeMonth=0,
            activeHalfyear=0
        )
    ),
    metadata={}
)

# DataBase
REDIS_POOL = redis.ConnectionPool(
    host=os.environ.get('WD_REDIS_SERVER', 'localhost'),
    port=os.environ.get('WD_REDIS_PORT', 6379),
    password=os.environ.get('WD_REDIS_PWD', None),
    max_connections=10
)
POSTGRES_POOL = create_engine(
    f"postgresql://{os.environ.get('WD_POSTGRES_USER', 'wand')}:{os.environ.get('WD_POSTGRES_PWD', 'password_of_wand')}@{os.environ.get('WD_POSTGRES_SERVER', 'localhost')}:{os.environ.get('WD_POSTGRES_PORT', '5432')}/{os.environ.get('WD_POSTGRES_DBNAME', 'wand')}",
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600
)
