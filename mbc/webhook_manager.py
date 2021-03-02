import typing
import discord
from .exceptions import *
from aiohttp import web


class Webhook:
    id: int

    def __init__(self, token: str, endpoint: str, trigger: str):
        self.token: str = token
        self.endpoint: str = endpoint
        self.trigger: str = trigger.lower()

        if self.trigger not in (
                "new_bot",
                "new_comment",
                "bot_edit_currently",
                "bot_edit",
                "bot_delete",
                "new_bump"
        ):
            raise ClientException("An invalid webhook trigger was provided")

    def __getitem__(self, item):
        return self.__getattribute__(item)


class WebhookManager:
    _webserver: web.TCPSite

    def __init__(self, bot: discord.Client, port: int, host: str):
        self.bot: discord.Client = bot
        self.webhooks: typing.List[Webhook] = []
        self.port: int = port
        self.host = host
        self.last_id: int = 0
        self.__app: web.Application = web.Application()
        self._is_closed: bool = False

    def add(self, webhook: Webhook) -> Webhook:
        webhook.id = self._generate_id()
        self.webhooks.append(webhook)
        return webhook

    def remove(self, webhook_id: int) -> typing.Optional[Webhook]:
        for webhook in self.webhooks:
            if webhook.id == webhook_id:
                self.webhooks.remove(webhook)
                return webhook
        return None

    def get_webhooks(self) -> typing.List[Webhook]:
        return self.webhooks

    def find(self, **kwargs):
        for webhook in self.webhooks:
            if all([webhook[key] == value for key, value in kwargs.items()]):
                return webhook

        return None

    def find_all(self, **kwargs):
        return [
            webhook
            for webhook in self.webhooks
            if all([webhook[key] == value for key, value in kwargs.items()])
        ]

    def _generate_id(self):
        new_id = self.last_id + 1
        self.last_id = new_id
        return new_id

    async def _handler(self, request: web.Request):
        data = await request.json()
        webhook = self.find(
            endpoint=str(request.rel_url),
            trigger=data.get("trigger")
        )
        if webhook is None:
            return web.Response(status=404, text="Not found")

        if request.headers.get("Authorization") != webhook.token:
            return web.Response(status=400, text="An invalid token was provided")

        self.bot.dispatch(data.get("trigger"), data)
        return web.Response(status=204)

    async def run(self):
        for webhook in self.webhooks:
            self.__app.router.add_post(webhook.endpoint, self._handler)

        runner = web.AppRunner(self.__app)
        await runner.setup()
        self._webserver = web.TCPSite(runner, self.host, self.port)
        await self._webserver.start()

    async def close(self):
        if self._is_closed:
            return

        await self._webserver.stop()
        self._is_closed = True