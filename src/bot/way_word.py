import asyncio

from bot.db.work_user import set_user_auth_state
from bot.db.work_word import delete_word, get_all_word, info_word
from bot.db.work_word import get_all_word
from bot.db.work_word import info_word
from bot.db.work_word import new_word
from bot.db.work_word import word_check_bd
from bot.send import Delete_message, Send_a_request_user
from bot.send import Send_a_request_user
from bot.telegram.types import Update
from bot.way_menu import main_menu


async def _info_word(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Команды настроек: \n"
        " 1 : Просмотр списка запрещенных слов  \n"
        " 2 : Добавление запрещенного слова \n"
        " 3 : Удаление слова из списка запрещенных \n"
        " Для возврата в предыдущее меню введите exit"
    )
    await set_user_auth_state(user_id, 14)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _work_info_word(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    text = update.message.text
    if text == "1":
        await set_user_auth_state(user_id, 13)
        await _all_word(update)
    if text == "2":
        await set_user_auth_state(user_id, 11)
        await _info_on_adding_a_word(update)
    if text == "3":
        await set_user_auth_state(user_id, 15)
        await _dell_word_info(update)
    if text == "exit":
        await main_menu(update)
    if (
        text != "1"
        and text != "2"
        and text != "3"
        and text != "exit"
        and text != None
    ):
        reply_to_message_id = "Вы ввели неверную команду, повторите ещё раз"
        await Send_a_request_user(
            chat_id=update.message.chat.id,
            text=reply_to_message_id,
        )
    return


async def _all_word(update: Update):
    reply_to_message_id = "Список слов: \n"
    list = await get_all_word()
    numbers = 1
    for i in list:
        word = await info_word(i)
        reply_to_message_id += f"{numbers} - {word}\n"
        len_message_id = len(reply_to_message_id)
        if len_message_id >= 4000:
            await Send_a_request_user(
                chat_id=update.message.chat.id,
                text=reply_to_message_id,
            )
            reply_to_message_id = ""
        numbers += 1
    user_id = update.message.from_.id
    await set_user_auth_state(user_id, 10)
    await _info_word(update)

    return


async def _info_on_adding_a_word(update: Update):
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Вы можете добавить слово список запрещенных.\n"
        "Для реализации данного действия напишите слово, или список слов через запятую.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 12)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _adding_a_word(update: Update):
    if update.message.text == "exit":
        await _info_word(update)
    else:
        list_word = (
            update.message.text.replace(
                ";",
                " ",
            )
            .replace(",", " ")
            .replace(".", " ")
            .replace("!", " ")
            .replace("*", " ")
            .split()
        )
        # list_word = update.message.text.split(",")
        for i in list_word:
            await new_word(i.upper())
        await Delete_message(update.message.chat.id, update.message.message_id)
    return


async def _dell_word_info(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Вы можете удалить слово из списока запрещенных.\n"
        "Для реализации данного действия напишите слово.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 16)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _dell_word(update: Update):
    if update.message.text == "exit":
        await _info_word(update)
        return
    else:

        word = await word_check_bd(update.message.text.upper())
        if word == True:
            await delete_word(update.message.text.upper())
            await Delete_message(
                update.message.chat.id, update.message.message_id
            )
    return


async def word_check(update: Update):
    try:
        list_word = (
            update.message.text.replace(
                ";",
                " ",
            )
            .replace(",", " ")
            .replace(".", " ")
            .replace("!", " ")
            .replace("*", " ")
            .split()
        )
        list_bd_id = await get_all_word()
        list_bd_word = []
        list_key = 0
        for i in list_bd_id:
            word = await info_word(i)
            list_bd_word.insert(list_key, word)
            list_key += 1

        result = await word_analysis(list_word, list_bd_word)
        if result == True:
            await Delete_message(
                update.message.chat.id, update.message.message_id
            )
            reply_to_message_id = (
                f"Уважаемый(ая) {update.message.from_.username} Ваше сообщение удалено. "
                f"Просим Вас не использовать мат в общении. "
                f"Спасибо за понимае!"
            )
            post = await Send_a_request_user(
                chat_id=update.message.chat.id,
                text=reply_to_message_id,
            )
            await asyncio.sleep(10)
            result = await Delete_message(
                update.message.chat.id, post.result["message_id"]
            )
        return result

    finally:
        return {"ok": True}


async def word_analysis(list_word: list, list_bd_word: list):

    for bd_word in list_bd_word:
        for user_word in list_word:
            if bd_word == user_word.upper():
                return True

    return False