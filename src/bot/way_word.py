from bot.db.work_user import set_user_auth_state
from bot.db.work_word import new_word
from bot.send import delete_message
from bot.send import send_a_request_user
from bot.telegram.types import Update


async def _info_on_adding_a_word(update: Update):
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Вы можете добавить слово список запрещенных.\n"
        "Для реализации данного действия напишите слово.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 6)
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _adding_a_word(update: Update):
    await new_word(update.message.text.upper())
    await delete_message(update.message.chat.id, update.message.message_id)
    return
