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

from model import activitypub_model

# Env
VERSION = os.environ.get('WD_VERSION', 'DEV')
SERVER_URL = os.environ.get('WD_SERVER_URL', 'localhost')

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
