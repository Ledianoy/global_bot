from bot.db.work import get_all_chenal
from bot.db.work import info_chenal
from bot.db.work import new_chenal
from bot.db.work_user import set_user_auth_state
from bot.send import delete_message
from bot.send import send_a_request_user
from bot.telegram.types import Update
from bot.way_menu import main_menu


async def _info_chenal(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Команды настроек: \n"
        " 1 : Просмотр списка запрещенных канало  \n"
        " 2 : Добавление запрещенного канала \n"
        " Для возврата в предыдущее меню введите exit"
    )
    await set_user_auth_state(user_id, 7)
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _work_info_chenal(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    text = update.message.text
    if text == "1":
        await set_user_auth_state(user_id, 6)
        await _all_chenal(update)
    if text == "2":
        await set_user_auth_state(user_id, 4)
        await _info_on_adding_a_channel(update)
    if text == "exit":
        await main_menu(update)
    if text != "1" and text != "2" and text != "exit" and text != None:
        reply_to_message_id = "Вы ввели неверную команту, повторите ещё раз"
        await send_a_request_user(
            chat_id=update.message.chat.id,
            text=reply_to_message_id,
        )
    return


async def _all_chenal(update: Update):
    reply_to_message_id = "Список каналов: \n"
    list = await get_all_chenal()
    for i in list:
        name_chenal = await info_chenal(i)
        reply_to_message_id += f"{i} - {name_chenal}\n"
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    user_id = update.message.from_.id
    await set_user_auth_state(user_id, 3)
    await _info_chenal(update)

    return


async def _info_on_adding_a_channel(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Вы можете добавить телеграм каналы в список запрещенных.\n"
        "Для реализации данного действия сделайте репист канал в бота.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 5)
    await send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _adding_a_channel(update: Update):
    if update.message.text == "exit":
        await _info_chenal(update)
    await new_chenal(
        update.message.forward_from_chat.id,
        update.message.forward_from_chat.title,
    )
    await delete_message(update.message.chat.id, update.message.message_id)
    return
