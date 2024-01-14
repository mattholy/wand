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
NODE_INFO_LINKS = activitypub_model.NodeinfoLinks(links=[
    activitypub_model.NodeinfoLink(
        rel="http://nodeinfo.diaspora.software/ns/schema/2.1",
        href=f"https://{SERVER_URL}/nodeinfo/2.1"
    )
])
NODE_INFO = activitypub_model.Nodeinfo(
    version="2.1",
    software=activitypub_model.NodeinfoSoftware(
        name="wand",
        version=VERSION,
        repository="https://github.com/mattholy/wand"
    ),
    protocols=["activitypub"],
    services={"inbound": [], "outbound": []},
    open_registrations=True,
    usage=activitypub_model.NodeinfoUsage(
        users=activitypub_model.NodeinfoUsageUsers(
            total=0,
            active_month=0,
            active_halfyear=0
        )
    ),
    metadata=activitypub_model.NodeinfoMetadata()
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
