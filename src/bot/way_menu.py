from bot.db.work_user import set_user_auth_state
from bot.send import Send_a_request_user
from bot.telegram.types import Update


async def main_menu(update: Update):
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Тебя узнали!\n"
        "Команды настроек: \n"
        " 1 : Работа с каналами \n"
        " 2 : Работа со словами"
    )

    await set_user_auth_state(user_id, 2)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return
