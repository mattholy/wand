# -*- encoding: utf-8 -*-
'''
activitypub_model.py
----
Data Model of ActivityPUB


@Time    :   2024/01/14 17:00:16
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from pydantic import BaseModel, AnyUrl, HttpUrl
from typing import List, Dict, Optional

class Link(BaseModel):
    rel: AnyUrl
    href: AnyUrl

class NodeInfoLinks(BaseModel):
    links: list[Link]

class Software(BaseModel):
    name: str
    version: str
    repository: HttpUrl

class Users(BaseModel):
    total: int
    activeMonth: int
    activeHalfyear: int

class Usage(BaseModel):
    users: Users

class NodeInfoModel(BaseModel):
    version: str
    software: Software
    protocols: List[str]
    services: Dict[str, List[str]]
    openRegistrations: bool
    usage: Usage
    metadata: Dict[str, Optional[str]]