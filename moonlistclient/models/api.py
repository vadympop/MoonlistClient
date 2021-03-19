import datetime
import typing

from pydantic import BaseModel
from moonlistclient.models.bases import BaseBot, RawBot, BaseComment, BaseServer


class Bot(BaseBot):
    bot_id: int


class Bump(BaseModel):
    id: int
    bot_id: int
    user_id: int
    time: datetime.datetime


class BumpsCount(BaseModel):
    count: int


class Comment(BaseComment):
    entity_id: int


class Report(BaseModel):
    id: int
    author_id: int
    entity_id: int
    created_at: datetime.datetime
    reason: str
    type: str
    state: int


class UserSocial(BaseModel):
    github: typing.Optional[str]
    website: typing.Optional[str]
    youtube: typing.Optional[str]
    discord: typing.Optional[str]
    twitter: typing.Optional[str]
    facebook: typing.Optional[str]
    vk: typing.Optional[str]


class User(BaseModel):
    id: int
    user_id: int
    access_level: int
    verificated: bool
    registered_at: datetime.datetime
    bio: typing.Optional[str]
    status: typing.Optional[str]
    bots: typing.List[RawBot] = []
    social: UserSocial
    badges: typing.List[str]


class Server(BaseServer):
    guild_id: int