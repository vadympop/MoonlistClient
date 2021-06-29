import typing
from pydantic import BaseModel
from moonlistclient.models.bases import RawBot, BotInEdit, BaseComment, BaseServer, ServerInEdit


class BaseWebhookModel(BaseModel):
    trigger: str
    type: str
    user_id: int
    entity_id: int


class NewBotWebhook(BaseWebhookModel):
    bot: RawBot


class BotDeleteWebhook(BaseWebhookModel):
    reason: str
    bot: RawBot


class BotEditWebhook(BaseWebhookModel):
    new_data: BotInEdit


class BotEditCurrentlyWebhook(BaseWebhookModel):
    comment: typing.Optional[str]
    currently: int


class NewBumpWebhook(BaseWebhookModel):
    count_bumps: int


class NewCommentWebhook(BaseWebhookModel):
    comment: BaseComment


class NewServerWebhook(BaseWebhookModel):
    server: BaseServer


class ServerDeleteWebhook(BaseWebhookModel):
    reason: str
    server: BaseServer


class ServerEditWebhook(BaseWebhookModel):
    new_data: ServerInEdit