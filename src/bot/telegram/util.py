from typing import TypeVar

from pydantic.main import BaseModel

from bot.config import settings
from bot.telegram.types import WebhookInfo

OutputDataT = TypeVar("OutputDataT", bound=BaseModel)


def shadow_webhook_secret(webhook: WebhookInfo) -> WebhookInfo:
    if not webhook.url:
        return webhook

    safe_url = webhook.url.replace(settings.webhook_secret, "")
    if safe_url.endswith("//"):
        safe_url = safe_url[:-1]

    result = webhook.copy(
        update={
            "url": safe_url,
        }
    )

    return result
