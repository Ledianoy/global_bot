from typing import Optional
from typing import TypeVar

import aiohttp
from pydantic import BaseModel

from bot.telegram.consts import TELEGRAM_BOT_API
from bot.telegram.types import DeleteMessage
from bot.telegram.types import SendMessage
from bot.telegram.types import TelegramResponse

OutputDataT = TypeVar("OutputDataT", bound=BaseModel)


async def Send_a_request_user(
    *,
    chat_id: int,
    text: str,
    reply_to_message_id: Optional[int] = None,
):
    reply = SendMessage(
        chat_id=chat_id,
        reply_to_message_id=reply_to_message_id,
        text=text,
    )

    result = await Send_api_telegram("sendMessage", reply)
    return result


async def Send_a_request_user_2(
    text: str,
):
    send = f"getChat?chat_id=@{text}"

    url = f"{TELEGRAM_BOT_API}/{send}"

    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            payload = await response.json()
    response_tg = TelegramResponse.parse_obj(payload)

    return response_tg


async def Delete_message(chat_id: int, message_id: int):
    reply_delete = DeleteMessage(
        chat_id=chat_id,
        message_id=message_id,
    )
    result = await Send_api_telegram("deleteMessage", reply_delete)

    return result


async def Send_api_telegram(
    method_name: str,
    data: Optional[BaseModel],
    # output_type: Optional[Type[OutputDataT]],
) -> Optional[OutputDataT]:
    url = f"{TELEGRAM_BOT_API}/{method_name}"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data.dict()) as response:
            payload = await response.json()
    response_tg = TelegramResponse.parse_obj(payload)
    return response_tg
