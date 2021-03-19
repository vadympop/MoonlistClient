import datetime
import typing
from moonlistclient.models.discord import DiscordUser, DiscordGuild
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


class BaseBot(BaseModel):
    id: int
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
    discord: DiscordUser
    owner: DiscordUser
    owners: typing.List[typing.Optional[DiscordUser]]


class RawBot(BaseBot):
    bot_id: int
    count_bumps: typing.Optional[int]
    discord: typing.Optional[DiscordUser]
    owner: int
    owners: typing.List[typing.Optional[int]]


class BotInEdit(BaseModel):
    short_description: typing.Optional[str]
    description: typing.Optional[str]
    invite: typing.Optional[str]
    prefix: typing.Optional[str]
    tags: typing.Optional[typing.List[str]]
    lib: typing.Optional[str]
    hidden: typing.Optional[bool]
    owners: typing.Optional[typing.List[int]]
    options: typing.Optional[BotOptions]
    badges: typing.Optional[typing.List[str]]
    pinned: typing.Optional[bool]
    verificated: typing.Optional[bool]


class BaseComment(BaseModel):
    id: int
    user_id: int
    mark: int
    created_at: datetime.datetime
    edited_at: typing.Optional[datetime.datetime]
    message: str


class BaseServer(BaseModel):
    id: int
    owner_id: int
    added_at: datetime.datetime
    invite: str
    short_description: str
    description: str
    features: dict
    tags: typing.List[str]
    discord: DiscordGuild


class ServerInEdit(BaseModel):
    invite: typing.Optional[str]
    short_description: typing.Optional[str]
    description: typing.Optional[str]
    tags: typing.Optional[typing.List[str]]