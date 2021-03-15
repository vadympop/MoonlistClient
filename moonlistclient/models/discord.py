import typing
from pydantic import BaseModel


class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: typing.Optional[str]
    discriminator: str
    public_flags: int
    bot: bool = False
