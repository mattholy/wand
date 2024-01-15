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

from pydantic import BaseModel, Field, AnyUrl, HttpUrl
from typing import List, Dict, Optional, Any


class PublicKey(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    owner: Optional[str] = Field(None, alias='owner')
    public_key_pem: Optional[str] = Field(None, alias='publicKeyPem')

    class Config:
        populate_by_name = True


class Endpoints(BaseModel):
    shared_inbox: Optional[str] = Field(None, alias='sharedInbox')

    class Config:
        populate_by_name = True


class Image(BaseModel):
    url: Optional[str] = Field(None, alias='url')

    class Config:
        populate_by_name = True


class Actor(BaseModel):
    context: Any = Field(..., alias='@context')
    id: Optional[str] = Field(None, alias='id')
    type: Optional[str] = Field(None, alias='type')
    name: Optional[str] = Field(None, alias='name')
    preferred_username: Optional[str] = Field(None, alias='preferredUsername')
    summary: Optional[str] = Field(None, alias='summary')
    inbox: Optional[str] = Field(None, alias='inbox')
    endpoints: Optional[Endpoints] = Field(None, alias='endpoints')
    public_key: Optional[PublicKey] = Field(None, alias='publicKey')
    icon: Optional[Image] = Field(None, alias='icon')
    image: Optional[Image] = Field(None, alias='image')

    class Config:
        populate_by_name = True


class Activity(BaseModel):
    context: Any = Field(..., alias='@context')
    id: Optional[str] = Field(None, alias='id')
    actor: Optional[str] = Field(None, alias='actor')
    type: Optional[str] = Field(None, alias='type')
    object: Any = Field(..., alias='object')
    to: Optional[List[str]] = Field(None, alias='to')
    cc: Optional[List[str]] = Field(None, alias='cc')

    class Config:
        populate_by_name = True


class Signature(BaseModel):
    type: Optional[str] = Field(None, alias='type')
    creator: Optional[str] = Field(None, alias='creator')
    created: Optional[str] = Field(None, alias='created')
    signature_value: Optional[str] = Field(None, alias='signatureValue')

    class Config:
        populate_by_name = True


class WebfingerLink(BaseModel):
    rel: Optional[str] = Field(None, alias='rel')
    type: Optional[str] = Field(None, alias='type')
    href: Optional[str] = Field(None, alias='href')

    class Config:
        populate_by_name = True


class WebfingerResource(BaseModel):
    subject: Optional[str] = Field(None, alias='subject')
    links: Optional[List[WebfingerLink]] = Field(None, alias='links')

    class Config:
        populate_by_name = True


class NodeinfoLink(BaseModel):
    rel: str = Field(..., alias='rel')
    href: str = Field(..., alias='href')

    class Config:
        populate_by_name = True


class NodeinfoLinks(BaseModel):
    links: List[NodeinfoLink] = Field(..., alias='links')

    class Config:
        populate_by_name = True


class NodeinfoSoftware(BaseModel):
    name: str = Field(..., alias='name')
    version: str = Field(..., alias='version')
    repository: Optional[str] = Field(None, alias='repository')

    class Config:
        populate_by_name = True


class NodeinfoServices(BaseModel):
    inbound: List[str] = Field(..., alias='inbound')
    outbound: List[str] = Field(..., alias='outbound')

    class Config:
        populate_by_name = True


class NodeinfoUsageUsers(BaseModel):
    total: int = Field(...)
    active_month: int = Field(..., alias='activeMonth')
    active_halfyear: int = Field(..., alias='activeHalfyear')

    class Config:
        populate_by_name = True


class NodeinfoUsage(BaseModel):
    users: NodeinfoUsageUsers = Field(..., alias='users')

    class Config:
        populate_by_name = True


class NodeinfoMetadata(BaseModel):
    pass

    class Config:
        populate_by_name = True


class Nodeinfo(BaseModel):
    version: str = Field(..., alias='version')
    software: NodeinfoSoftware = Field(..., alias='software')
    protocols: List[str] = Field(..., alias='protocols')
    services: NodeinfoServices = Field(..., alias='services')
    open_registrations: bool = Field(..., alias='openRegistrations')
    usage: NodeinfoUsage = Field(..., alias='usage')
    metadata: NodeinfoMetadata = Field(..., alias='metadata')

    class Config:
        populate_by_name = True


class NodeinfoResources(BaseModel):
    nodeinfo_links: NodeinfoLinks = Field(..., alias='nodeinfoLinks')
    nodeinfo: Nodeinfo = Field(..., alias='nodeinfo')

    class Config:
        populate_by_name = True
