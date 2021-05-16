from bot.db.work import new_chenal
from bot.db.work_user import set_user_auth_state
from bot.send import delete_message
from bot.send import send_a_request_user
from bot.telegram.types import Update


async def _info_on_adding_a_channel(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Вы можете добавить телеграм каналы в список запрещенных.\n"
        "Для реализации данного действия сделайте репист канал в бота.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 4)
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _adding_a_channel(update: Update):
    await new_chenal(
        update.message.forward_from_chat.id,
        update.message.forward_from_chat.title,
    )
    await delete_message(update.message.chat.id, update.message.message_id)
    return
