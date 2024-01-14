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
from typing import List, Dict, Optional, Any


class PublicKey(BaseModel):
    id: Optional[str]
    owner: Optional[str]
    public_key_pem: Optional[str]

class Endpoints(BaseModel):
    shared_inbox: Optional[str]

class Image(BaseModel):
    url: Optional[str]

class Actor(BaseModel):
    context: Any
    id: Optional[str]
    type: Optional[str]
    name: Optional[str]
    preferred_username: Optional[str]
    summary: Optional[str]
    inbox: Optional[str]
    endpoints: Optional[Endpoints]
    public_key: Optional[PublicKey]
    icon: Optional[Image]
    image: Optional[Image]

class Activity(BaseModel):
    context: Any
    id: Optional[str]
    actor: Optional[str]
    type: Optional[str]
    object: Any
    to: Optional[List[str]]
    cc: Optional[List[str]]

class Signature(BaseModel):
    type: Optional[str]
    creator: Optional[str]
    created: Optional[str]
    signature_value: Optional[str]

class WebfingerLink(BaseModel):
    rel: Optional[str]
    type: Optional[str]
    href: Optional[str]

class WebfingerResource(BaseModel):
    subject: Optional[str]
    links: Optional[List[WebfingerLink]]

class NodeinfoLink(BaseModel):
    rel: str
    href: str

class NodeinfoLinks(BaseModel):
    links: List[NodeinfoLink]

class NodeinfoSoftware(BaseModel):
    name: str
    version: str
    repository: Optional[str]

class NodeinfoServices(BaseModel):
    inbound: List[str]
    outbound: List[str]

class NodeinfoUsageUsers(BaseModel):
    total: int
    active_month: int
    active_halfyear: int

class NodeinfoUsage(BaseModel):
    users: NodeinfoUsageUsers

class NodeinfoMetadata(BaseModel):
    pass

class Nodeinfo(BaseModel):
    version: str
    software: NodeinfoSoftware
    protocols: List[str]
    services: NodeinfoServices
    open_registrations: bool
    usage: NodeinfoUsage
    metadata: NodeinfoMetadata

class NodeinfoResources(BaseModel):
    nodeinfo_links: NodeinfoLinks
    nodeinfo: Nodeinfo