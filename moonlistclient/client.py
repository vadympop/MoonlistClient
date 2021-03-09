import asyncio
import discord
from .schemas import *
from .http import ApiClient
from .exceptions import *
from .webhook_manager import WebhookManager


class MoonlistClient:
    _autopost_loop: asyncio.Task
    webhook_manager: WebhookManager

    def __init__(self, bot: discord.Client, api_key: str, autopost: bool = True, **kwargs):
        self.bot: discord.Client = bot
        self.loop: asyncio.AbstractEventLoop = kwargs.get("loop", self.bot.loop)
        self.autopost: bool = autopost
        self.http: ApiClient = kwargs.get("api_client", ApiClient(api_key))
        self._is_closed: bool = False

        if kwargs.get("webhook", False):
            self.webhook_manager = kwargs.get("webhook_manager", WebhookManager(
                bot=self.bot,
                port=kwargs.get("port", 5000),
                host=kwargs.get("host", "0.0.0.0")
            ))

        if self.autopost:
            self._autopost_loop = self.loop.create_task(self.autopost_loop())

    async def autopost_loop(self):
        while self.bot.is_ready():
            try:
                await self.post_stat()
            except HTTPException:
                pass
            await asyncio.sleep(10800)

    async def post_stat(self):
        await self.http.post_bot_stat(
            bot_id=self.bot.user.id,
            guilds=len(self.bot.guilds),
            users=len(self.bot.users),
            shards=self.bot.shard_count or 0
        )
        await self.bot.dispatch("post_stat")

    async def get_bot(self, bot_id: int) -> Bot:
        return Bot(**await self.http.get_bot(bot_id))

    async def get_bots(self, limit: int = 20, skip: int = 0) -> typing.List[Bot]:
        return list(map(lambda item: Bot(**item), await self.http.get_bots(limit, skip)))

    async def get_bumps(self, bot_id: int) -> typing.List[Bump]:
        return list(map(lambda item: Bump(**item), await self.http.get_bumps(bot_id)))

    async def get_bumps_count(self, bot_id: int) -> BumpsCount:
        return BumpsCount(**await self.http.get_bumps_count(bot_id))

    async def get_comments(self, bot_id: int) -> typing.List[Comment]:
        return list(map(lambda item: Comment(**item), await self.http.get_comments(bot_id)))

    async def get_user_reports(self, user_id: int) -> typing.List[Report]:
        return list(map(lambda item: Report(**item), await self.http.get_user_reports(user_id)))

    async def get_reports(self) -> typing.List[Report]:
        return list(map(lambda item: Report(**item), await self.http.get_reports()))

    async def get_user(self, user_id: int) -> User:
        return await self.get_user(user_id)

    async def get_user_bots(self, user_id: int) -> typing.List[Bot]:
        return list(map(lambda item: Bot(**item), await self.http.get_user_bots(user_id)))

    async def get_bot_stats(self, bot_id: int) -> typing.List[BotStat]:
        return list(map(lambda item: BotStat(**item), await self.http.get_bot_stats(bot_id)))

    async def get_bot_stat(self, bot_id: int) -> BotStat:
        return BotStat(**await self.http.get_bot_stat(bot_id))

    async def get_servers(self) -> typing.List[Server]:
        return list(map(lambda item: Server(**item), await self.http.get_servers()))

    async def get_server(self, guild_id: int) -> Server:
        return Server(**await self.http.get_server(guild_id))

    async def close(self):
        if self._is_closed:
            return

        await self.http.close()
        if self._autopost_loop is not None:
            self._autopost_loop.cancel()

        if self.webhook_manager is not None:
            await self.webhook_manager.close()

        self._is_closed = True