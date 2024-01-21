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

from pydantic import BaseModel, ConfigDict, Field, AnyUrl, HttpUrl
from typing import List, Dict, Optional, Any


class PublicKey(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    owner: Optional[str] = Field(None, alias='owner')
    public_key_pem: Optional[str] = Field(None, alias='publicKeyPem')

    class Config:
        populate_by_name = True


class Endpoints(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    shared_inbox: Optional[str] = Field(None, alias='sharedInbox')


class Image(BaseModel):
    url: Optional[str] = Field(None, alias='url')

    class Config:
        populate_by_name = True


class Actor(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

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


class Activity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    context: Any = Field(..., alias='@context')
    id: Optional[str] = Field(None, alias='id')
    actor: Optional[str] = Field(None, alias='actor')
    type: Optional[str] = Field(None, alias='type')
    object: Any = Field(..., alias='object')
    to: Optional[List[str]] = Field(None, alias='to')
    cc: Optional[List[str]] = Field(None, alias='cc')


class Signature(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Optional[str] = Field(None, alias='type')
    creator: Optional[str] = Field(None, alias='creator')
    created: Optional[str] = Field(None, alias='created')
    signature_value: Optional[str] = Field(None, alias='signatureValue')


class WebfingerLink(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    rel: Optional[str] = Field(None, alias='rel')
    type: Optional[str] = Field(None, alias='type')
    href: Optional[str] = Field(None, alias='href')


class WebfingerResource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    aliases: Optional[str] = Field(None, alias='aliases')
    subject: Optional[str] = Field(None, alias='subject')
    links: Optional[List[WebfingerLink]] = Field(None, alias='links')


class NodeinfoLink(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    rel: str = Field(..., alias='rel')
    href: str = Field(..., alias='href')


class NodeinfoLinks(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    links: List[NodeinfoLink] = Field(..., alias='links')


class NodeinfoSoftware(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., alias='name')
    version: str = Field(..., alias='version')
    repository: Optional[str] = Field(None, alias='repository')


class NodeinfoServices(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    inbound: List[str] = Field(..., alias='inbound')
    outbound: List[str] = Field(..., alias='outbound')


class NodeinfoUsageUsers(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total: int = Field(...)
    active_month: int = Field(..., alias='activeMonth')
    active_halfyear: int = Field(..., alias='activeHalfyear')


class NodeinfoUsage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    users: NodeinfoUsageUsers = Field(..., alias='users')


class NodeinfoMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pass


class Nodeinfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    version: str = Field(..., alias='version')
    software: NodeinfoSoftware = Field(..., alias='software')
    protocols: List[str] = Field(..., alias='protocols')
    services: NodeinfoServices = Field(..., alias='services')
    openRegistrations: bool = Field(..., alias='open_registrations')
    usage: NodeinfoUsage = Field(..., alias='usage')
    metadata: NodeinfoMetadata = Field(..., alias='metadata')


class NodeinfoResources(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nodeinfo_links: NodeinfoLinks = Field(..., alias='nodeinfoLinks')
    nodeinfo: Nodeinfo = Field(..., alias='nodeinfo')
