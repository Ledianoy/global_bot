import enum
import os

from bot.db.work_user import get_user
from bot.db.work_user import init_user
from bot.db.work_user import set_user_auth_state
from bot.send import Send_api_telegram
from bot.send import send_a_request_user
from bot.telegram.types import Update
from bot.way_chenal import _adding_a_channel
from bot.way_chenal import _info_on_adding_a_channel
from bot.way_word import _adding_a_word
from bot.way_word import _info_on_adding_a_word


@enum.unique
class AuthState(enum.Enum):
    UNKNOWN = None
    WAITING_FOR_PASSWORD = 1
    AUTHENTICATED = 2
    INFO_ADDING_A_CHANNEL = 3
    ADDING_A_CHANNEL = 4
    ADDING_A_WORD = 6


async def process_way(update: Update):
    dispatcher_value = {
        1: _process_password(update),
        2: _choice_of_functionality(update),
        3: _info_on_adding_a_channel(update),
        4: _adding_a_channel(update),
        5: _info_on_adding_a_word(update),
        6: _adding_a_word(update),
    }
    dispatcher_text = {
        "/exit": exit(update),
        "/base": base(update),
        "/start": start(update),
    }

    user_id = update.message.from_.id
    state = await get_state(user_id)
    for key, value in dispatcher_value.items():
        if key == state.value:
            await value
    for key, value in dispatcher_text.items():
        if key == update.message.text:
            await value

    return {"ok": True}


async def base(update: Update):
    user_id = update.message.from_.id
    await init_user(user_id)
    state = await get_state(user_id)
    if state.name == "UNKNOWN":
        reply_to_message_id = "Введите пароль"
        await set_user_auth_state(user_id, 1)
        await send_a_request_user(
            chat_id=update.message.chat.id,
            text=reply_to_message_id,
        )
        await Send_api_telegram("SendMessage", send_a_request_user)


async def exit(update: Update):
    await init_user(update.message.from_.id)
    await set_user_auth_state(update.message.from_.id, None)
    reply_to_message_id = "Спасибо за работу!"
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    await Send_api_telegram("SendMessage", send_a_request_user)


async def get_state(user_id: int) -> AuthState:
    user = await get_user(user_id)
    if not user:
        return AuthState.UNKNOWN

    try:
        state = AuthState(user.state_auth)
    except ValueError:
        state = AuthState.UNKNOWN

    return state


async def _process_password(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    password = update.message.text
    user = await get_user(user_id)

    pass_user = False
    if user and password:
        if password == os.getenv("PASSWORD"):
            pass_user = True

    if pass_user == False:
        reply_to_message_id = (
            "Аутентификация провалена.\n"
            "Попробуем ещё раз.\n"
            "Повторно введите команду доступа к базе"
        )
        await set_user_auth_state(user_id,None)
        await send_a_request_user(
            chat_id=update.message.chat.id,
            text=reply_to_message_id,
        )
        return

    reply_to_message_id = (
        "Тебя узнали!\n"
        "Команды настроек: \n"
        " 1 : Добавление канала \n"
        " 2 : Добавление запрещенного слова"
    )

    await set_user_auth_state(user_id, 2)
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _choice_of_functionality(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    if update.message.text == "1":
        await set_user_auth_state(user_id, 3)
        await _info_on_adding_a_channel(update)
    if update.message.text == "2":
        await set_user_auth_state(user_id, 5)
        await _info_on_adding_a_word(update)


async def start(update: Update):
    await init_user(update.message.from_.id)
    await set_user_auth_state(update.message.from_.id,None)
    reply_to_message_id = "Функции бота"
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    m = await Send_api_telegram("SendMessage", send_a_request_user)
