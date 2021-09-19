import asyncio
import os

import docx
import requests

from bot.db.work import delete_chenal
from bot.db.work import get_all_chenal
from bot.db.work import id_chenal
from bot.db.work import info_chenal
from bot.db.work import new_chenal
from bot.db.work_user import set_user_auth_state
from bot.send import Delete_message
from bot.send import Send_a_request_chat_id
from bot.send import Send_a_request_user
from bot.telegram.types import Update
from bot.way_menu import main_menu


async def _info_chenal(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Команды настроек: \n"
        " 1 : Просмотр списка запрещенных каналов  \n"
        " 2 : Добавление запрещенного канала \n"
        " 3 : Удаление канала из списка запрещенных \n"
        " 4 : Анализ республиканского списока экстремистских материалов"
        " Для возврата в предыдущее меню введите exit"
    )
    await set_user_auth_state(user_id, 7)
    await Send_a_request_user(
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
    if text == "3":
        await set_user_auth_state(user_id, 8)
        await _dell_chenal_info(update)
    if text == "4":
        await set_user_auth_state(user_id, 17)
        await _registry(update)
    if text == "exit":
        await main_menu(update)
    if (
        text != "1"
        and text != "2"
        and text != "3"
        and text != "exit"
        and text != None
    ):
        reply_to_message_id = "Вы ввели неверную команту, повторите ещё раз"
        await Send_a_request_user(
            chat_id=update.message.chat.id,
            text=reply_to_message_id,
        )
    return


async def _dell_chenal_info(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = (
        "Вы можете удалить телеграм каналы из списока запрещенных.\n"
        "Для реализации данного действия сделайте репист канала в бота или вставте Ссылку-приглашение.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 9)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _dell_chenal(update: Update):
    if update.message.text == "exit":
        await _info_chenal(update)
    elif update.message.forward_from_chat == None:
        text = update.message.text.split("/")
        if text[0] == "https:":
            info = await Send_a_request_chat_id(text[-1])
            id = info.result["id"]
            title = info.result["title"]
    else:
        id = update.message.forward_from_chat.id
        title = update.message.forward_from_chat.title
    chenal = await id_chenal(id, title)
    if chenal == True:
        await delete_chenal(id)
        await Delete_message(update.message.chat.id, update.message.message_id)
    return


async def _all_chenal(update: Update):
    reply_to_message_id = "Список каналов: \n"
    list_chenal = await get_all_chenal()
    number = 1
    for lists in list_chenal:
        name_chenal = await info_chenal(lists)
        reply_to_message_id += f"{number}: {lists} - {name_chenal}\n"
        len_message_id = len(reply_to_message_id)
        if len_message_id >= 4000:
            await Send_a_request_user(
                chat_id=update.message.chat.id,
                text=reply_to_message_id,
            )
            reply_to_message_id = ""
        number += 1
    await Send_a_request_user(
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
        "Для реализации данного действия сделайте репист канала в бота или вставте Ссылку-приглашение.\n"
        "Для выхода введите команду exit"
    )
    await set_user_auth_state(user_id, 5)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def _adding_a_channel(update: Update):
    if update.message.text == "exit":
        await _info_chenal(update)
    elif update.message.forward_from_chat is None:
        text = update.message.text.split("/")
        if text[0] == "https:":
            info = await Send_a_request_chat_id(text[-1])
            if info.ok != True:
                return
            else:
                id = info.result["id"]
                title = info.result["title"]
    else:
        id = update.message.forward_from_chat.id
        title = update.message.forward_from_chat.title
    await new_chenal(
        id,
        title,
    )
    await Delete_message(update.message.chat.id, update.message.message_id)
    return


async def repost_chanel(update):
    try:
        chenal_bloc = await id_chenal(
            update.message.forward_from_chat.id,
            update.message.forward_from_chat.title,
        )
        if chenal_bloc == True:
            result = await Delete_message(
                update.message.chat.id, update.message.message_id
            )
            reply_to_message_id = (
                f"Уважаемый(ая) {update.message.from_.username} Ваш репост удален. "
                f"Данный телеграм канал запрещенн на терриории РБ"
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


async def _registry(update: Update):
    assert update.message.from_
    user_id = update.message.from_.id
    reply_to_message_id = "Для анализа республиканского списка экстремистских материалов укажите ссылку на DOC файл."
    await set_user_auth_state(user_id, 18)
    await Send_a_request_user(
        chat_id=update.message.chat.id,
        text=reply_to_message_id,
    )
    return


async def api_chenel(update):
    if update.message.text == "exit":
        await _info_chenal(update)
    elif update.message.forward_from_chat is None:
        text = update.message.text.split("/")
        file_docx = text[-1]
        save_link(update.message.text, file_docx)
        wordDoc = docx.Document(file_docx)
        allText = []
        for table in wordDoc.tables:
            for row in table.rows:
                for cell in row.cells:
                    allText.append(cell.text)
        urltme = []
        for text_len in allText:
            list_word = (
                text_len.replace(
                    ";",
                    " ",
                )
                .replace(",", " ")
                .replace("!", " ")
                .replace("*", " ")
                .split()
            )
            for text in list_word:
                temp = len(text)
                if temp > 10:
                    temp_text = text[0:12]
                    if temp_text == "https://t.me":
                        if text[-1] == ".":
                            url_len = len(text)
                            urltme.append(text[0 : url_len - 1])
                        else:
                            urltme.append(text)

        i = 0
        os.remove(file_docx)
        list_chenal = []
        len_list = len(urltme) - 1
        while i <= len_list:
            url = urltme[i]
            text_url = url.split("/")
            info = await Send_a_request_chat_id(text_url[-1])
            if info.ok != True:
                i += 1
            else:
                id = info.result["id"]
                title = info.result["title"]
                chenal_bloc = await id_chenal(id, title)
                if chenal_bloc != True:
                    list_chenal.append(id)
                    await new_chenal(id, title)
                i += 1
        reply_to_message_id = "Список каналов: \n"
        number = 1
        for lists in list_chenal:
            name_chenal = await info_chenal(lists)
            reply_to_message_id += f"{number}: {lists} - {name_chenal}\n"
            len_message_id = len(reply_to_message_id)
            if len_message_id >= 4000:
                await Send_a_request_user(
                    chat_id=update.message.chat.id,
                    text=reply_to_message_id,
                )
                reply_to_message_id = ""
            number += 1
        await Send_a_request_user(
            chat_id=update.message.chat.id,
            text=reply_to_message_id,
        )
        user_id = update.message.from_.id
        await set_user_auth_state(user_id, 3)
        await _info_chenal(update)
    return


def save_link(book_link, book_name):
    the_book = requests.get(book_link, stream=True)
    with open(book_name, "wb") as f:
        for chunk in the_book.iter_content(1024 * 1024 * 2):  # 2 MB chunks
            f.write(chunk)
    return
