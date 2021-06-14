from typing import Optional
from ..send import Send_api_telegram
from .types import Message
from .types import SendMessage
from .types import SetWebhook
from .types import WebhookInfo


async def send_message(
    *,
    chat_id: int,
    text: str,
    reply_to_message_id: Optional[int] = None,
) -> Message:
    reply = SendMessage(
        chat_id=chat_id,
        reply_to_message_id=reply_to_message_id,
        text=text,
    )

    message = await Send_api_telegram("sendMessage", reply, Message)
    assert message is not None

    return message


async def set_webhook(
    *,
    url: str,
) -> None:
    webhook = SetWebhook(
        drop_pending_updates=True,
        url=url,
    )

    await Send_api_telegram("setWebhook", webhook, None)


async def get_webhook_info() -> WebhookInfo:
    webhook_info = await Send_api_telegram("getWebhookInfo", None, WebhookInfo)
    assert webhook_info is not None

    return webhook_info

