import datetime
import typing
from moonlistclient.models.discord import DiscordUser
from pydantic import BaseModel


class BotStat(BaseModel):
    id: int
    time: datetime.datetime
    bot_id: int
    users: int
    guilds: int
    shards: int


class BotOptions(BaseModel):
    github: typing.Optional[str]
    website: typing.Optional[str]
    documentation: typing.Optional[str]
    support_server: typing.Optional[str]


class Bot(BaseModel):
    id: int
    bot_id: int
    currently: int
    added_at: datetime.datetime
    short_description: str
    description: str
    invite: str
    prefix: str
    tags: list
    lib: str
    hidden: bool
    pinned: bool
    options: BotOptions
    badges: list
    verificated: bool
    stat: typing.Optional[BotStat]
    count_bumps: int
    discord: dict
    owner: DiscordUser
    owners: typing.List[typing.Optional[DiscordUser]]


class Bump(BaseModel):
    id: int
    bot_id: int
    user_id: int
    time: datetime.datetime


class BumpsCount(BaseModel):
    count: int


class Comment(BaseModel):
    id: int
    bot_id: int
    user_id: int
    mark: int
    created_at: datetime.datetime
    edited_at: typing.Optional[datetime.datetime]
    message: str


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
    bots: list = []
    social: UserSocial
    badges: list


class Server(BaseModel):
    id: int
    guild_id: int
    owner_id: int
    added_at: datetime.datetime
    invite: str
    short_description: str
    description: str
    features: dict
    tags: list