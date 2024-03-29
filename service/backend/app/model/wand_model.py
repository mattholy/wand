# -*- encoding: utf-8 -*-
'''
wand_model.py
----
Data model of wand system


@Time    :   2024/01/15 19:09:25
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import redis
import typing
import uuid
from redis_om import HashModel, Field
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Text, TIMESTAMP, func, Integer, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import UniqueConstraint, Index

from ..wand_env import REDIS_POOL, SERVER_URL

#############
#           #
# Redis ORM #
#           #
#############


class WandRelay(HashModel):
    wand_id: str = str(uuid.uuid4())
    actor_key_sec: str
    actor_key_pub: str
    service_domain: str = SERVER_URL
    service_name: str
    service_desc: str
    service_icon: str = ""
    service_image: str = ""
    admin_gpg_public_key: str
    agreements: str = 'False'

    class Meta:
        database = redis.Redis(connection_pool=REDIS_POOL)

############
#          #
# Wand API #
#          #
############


class WandInit(BaseModel):
    service_name: str
    service_desc: str
    admin_gpg_public_key: str
    agreements: bool


##########
#        #
# DB ORM #
#        #
##########
Base = declarative_base()


class Subscriber(Base):
    __tablename__ = 'ap_subscriber'

    server_id = Column(Text, unique=True, primary_key=True)
    name = Column(Text)
    desc = Column(Text)
    icon = Column(Text)
    inbox = Column(Text)
    software = Column(Text)
    status = Column(Text, nullable=False)
    subscription_return_msg = Column(Text)
    instance = Column(JSONB)
    nodeinfo = Column(JSONB)
    create_time = Column(TIMESTAMP(timezone=True), default=func.now())
    update_time = Column(TIMESTAMP(timezone=True),
                         onupdate=func.now(), default=func.now())

    __table_args__ = (
        Index('idx_instance_gin', 'instance', postgresql_using='gin'),
        Index('idx_nodeinfo_gin', 'nodeinfo', postgresql_using='gin'),
    )


class Activity(Base):
    __tablename__ = 'ap_activity'

    record_id = Column(BigInteger, primary_key=True, autoincrement=True)
    activity_id = Column(Text, unique=True, nullable=False)
    server_id = Column(Text, nullable=False)
    sender_id = Column(Text, nullable=False)
    data = Column(JSONB)
    receive_time = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_data_gin', 'data', postgresql_using='gin'),
    )


class MessageSendRecord(Base):
    __tablename__ = 'ap_message_send_record'

    record_id = Column(BigInteger, primary_key=True, autoincrement=True)
    activity_id = Column(Text, nullable=False)
    destnation_server_id = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    create_time = Column(TIMESTAMP(timezone=True), server_default=func.now())
