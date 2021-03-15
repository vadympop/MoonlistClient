import typing
import discord
from .models import webhooks
from .exceptions import *
from aiohttp import web


TRIGGER_TO_MODEl = {
    "new_bot": webhooks.NewBotWebhook,
    "new_comment": webhooks.NewCommentWebhook,
    "bot_edit_currently": webhooks.BotEditCurrentlyWebhook,
    "bot_edit": webhooks.BotEditWebhook,
    "bot_delete": webhooks.BotDeleteWebhook,
    "new_bump": webhooks.NewBumpWebhook,
    "new_server": webhooks.NewServerWebhook,
    "server_edit": webhooks.ServerEditWebhook,
    "server_delete": webhooks.ServerDeleteWebhook
}


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
            "new_bump",
            "new_server",
            "server_edit",
            "server_delete"
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
        self._last_id: int = 0
        self._app: web.Application = web.Application()
        self._is_ran: bool = False

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
        new_id = self._last_id + 1
        self._last_id = new_id
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

        self.bot.dispatch(data.get("trigger"), TRIGGER_TO_MODEl[data.get("trigger")](**data))
        return web.Response(status=204)

    async def run(self):
        if not self._is_ran:
            self._is_ran = True
            for webhook in self.webhooks:
                self._app.router.add_post(webhook.endpoint, self._handler)

            runner = web.AppRunner(self._app)
            await runner.setup()
            self._webserver = web.TCPSite(runner, self.host, self.port)
            await self._webserver.start()

    async def close(self):
        if not self._is_ran:
            return

        await self._webserver.stop()
        self._is_ran = False