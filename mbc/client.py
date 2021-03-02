import asyncio
from discord.ext import commands
from .http import ApiClient
from .exceptions import *
from .webhook_manager import WebhookManager


class MoonbotsClient:
    _autopost_loop: asyncio.Task
    webhook_manager: WebhookManager

    def __init__(self, bot: commands.Bot, api_key: str, autopost: bool = True, **kwargs):
        self.bot: commands.Bot = bot
        self.loop: asyncio.AbstractEventLoop = kwargs.get("loop") or self.bot.loop
        self.autopost: bool = autopost
        self.http: ApiClient = ApiClient(api_key)
        self._is_closed: bool = False

        if kwargs.get("webhook", default=False):
            self.webhook_manager = WebhookManager(
                bot=self.bot,
                port=kwargs.get("port", default=5000),
                host=kwargs.get("host", default="0.0.0.0")
            )

        if self.autopost:
            self._autopost_loop = self.loop.create_task(self.autopost_loop())

    async def autopost_loop(self):
        while self.bot.is_ready():
            try:
                await self.http.post_bot_stat(
                    bot_id=self.bot.user.id,
                    guilds=len(self.bot.guilds),
                    users=len(self.bot.users),
                    shards=self.bot.shard_count or 0
                )
                await self.bot.dispatch("post_stat")
            except HTTPException:
                pass
            await asyncio.sleep(10800)

    async def get_bot(self, bot_id: int):
        return await self.http.get_bot(bot_id)

    async def get_bots(self, limit: int = 20, skip: int = 0):
        return await self.http.get_bots(limit, skip)

    async def get_bumps(self, bot_id: int):
        return await self.http.get_bumps(bot_id)

    async def get_bumps_count(self, bot_id: int):
        return await self.http.get_bumps_count(bot_id)

    async def get_comments(self, bot_id: int):
        return await self.http.get_comments(bot_id)

    async def get_user_reports(self, user_id: int):
        return await self.http.get_user_reports(user_id)

    async def get_reports(self):
        return await self.http.get_reports()

    async def get_user(self, user_id: int):
        return await self.get_user(user_id)

    async def get_user_bots(self, user_id: int):
        return await self.http.get_user_bots(user_id)

    async def get_bot_stats(self, bot_id: int):
        return await self.http.get_bot_stats(bot_id)

    async def get_bot_stat(self, bot_id: int):
        return await self.http.get_bot_stat(bot_id)

    async def close(self):
        if self._is_closed:
            return

        await self.http.close()
        if self._autopost_loop is not None:
            self._autopost_loop.cancel()

        if self.webhook_manager is not None:
            await self.webhook_manager.close()

        self._is_closed = True