from pydantic import BaseModel


class BaseWebhookModel(BaseModel):
    trigger: str
    type: str
    user_id: int
    entity_id: int


class NewBotWebhook(BaseWebhookModel):
    bot: dict


class BotDeleteWebhook(BaseWebhookModel):
    reason: str
    bot: dict


class BotEditWebhook(BaseWebhookModel):
    new_data: dict


class BotEditCurrentlyWebhook(BaseWebhookModel):
    reason: str
    currently: int


class NewBumpWebhook(BaseWebhookModel):
    count_bumps: int


class NewCommentWebhook(BaseWebhookModel):
    comment: dict


class NewServerWebhook(BaseWebhookModel):
    server: dict


class ServerDeleteWebhook(BaseWebhookModel):
    reason: str
    server: dict


class ServerEditWebhook(BaseWebhookModel):
    new_data: dict