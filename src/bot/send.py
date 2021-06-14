from typing import Optional
from typing import Type
from typing import TypeVar

import aiohttp
from aiohttp import ClientResponse
from pydantic import BaseModel
from starlette import status

from bot.telegram.consts import TELEGRAM_BOT_API
from bot.telegram.types import DeleteMessage
from bot.telegram.types import SendMessage
from bot.telegram.types import TelegramResponse
from bot.util import debug

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

    result = await Send_api_telegram("sendMessage", reply, None)
    return result


async def Send_a_request_chat_id(
    text: str,
):
    send = f"getChat?chat_id=@{text}"
    result = await Send_api_telegram(send, None, None)
    return result


async def Delete_message(chat_id: int, message_id: int):
    reply_delete = DeleteMessage(
        chat_id=chat_id,
        message_id=message_id,
    )
    result = await Send_api_telegram("deleteMessage", reply_delete, None)

    return result


async def Send_api_telegram(
    method_name: str,
    data: Optional[BaseModel],
    output_type: Optional[Type[OutputDataT]],
) -> Optional[OutputDataT]:
    url = f"{TELEGRAM_BOT_API}/{method_name}"
    request_kw = {}

    if data is not None:
        request_kw.update(
            dict(
                json=data.dict(),
            )
        )

    async with aiohttp.ClientSession() as session:
        async with session.post(url, **request_kw) as response:
            payload = await response.json()
        if response.status != status.HTTP_200_OK:
            debug(response)
            debug(payload)
            errmsg = (
                f"method {method_name!r}"
                f" failed with status {response.status}"
            )
            raise RuntimeError(errmsg)

    response_tg = TelegramResponse.parse_obj(payload)

    if not response_tg.ok:
        debug(response_tg)
        errmsg = f"method {method_name!r} failed: {response_tg.result}"
        raise RuntimeError(errmsg)

    result = response_tg

    if output_type is not None:
        result = output_type.parse_obj(response_tg.result)

    return result
