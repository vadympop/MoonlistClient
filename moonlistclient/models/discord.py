import typing
from pydantic import BaseModel


class DiscordEmoji(BaseModel):
    name: str
    id: str
    animated: bool


class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: typing.Optional[str]
    discriminator: str
    public_flags: int
    bot: bool = False


class DiscordGuild(BaseModel):
    id: str
    name: str
    icon: typing.Optional[str]
    approximate_member_count: int
    approximate_presence_count: int
    region: str
    banner: typing.Optional[str]
    emojis: typing.List[DiscordEmoji]