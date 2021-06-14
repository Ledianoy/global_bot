import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from bot.config import settings
from bot.db.work import id_chenal
from bot.db.work_word import get_all_word
from bot.db.work_word import info_word
from bot.db.work_word import word_check_bd
from bot.send import Delete_message
from bot.send import Send_a_request_user
from bot.send import get_webhook_info
from bot.send import set_webhook
from bot.telegram.types import Update
from bot.telegram.util import shadow_webhook_secret
from bot.util import debug
from bot.way import process_way

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory=settings.index_path)


@app.get("/", response_class=HTMLResponse)
async def handle_index(request: Request):
    webhook_unsafe = await get_webhook_info()
    debug(webhook_unsafe)

    webhook_safe = shadow_webhook_secret(webhook_unsafe)

    context = {
        "url_webhook_current": webhook_safe.url,
        "url_webhook_new": f"{settings.service_url}/webhook/",
    }

    response = templates.TemplateResponse(
        "index.html", {"request": request, **context}
    )

    return response


@app.post("/webhook-setup/")
async def handle_setup_webhook(password: str = Form(...)):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin is allowed to configure webhook",
        )

    new_webhook_url = (
        f"{settings.service_url}/webhook/{settings.webhook_secret}/"
    )
    debug(new_webhook_url)

    await set_webhook(url=new_webhook_url)

    return RedirectResponse(
        "/",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.post(f"/webhook/{settings.webhook_secret}/")
async def tg_webhook(update: Update):
    debug(settings)
    try:
        if update.message.chat.type == "private":
            result = await process_way(update)
        if update.message.forward_from_chat is not None:
            result = await repost_chanel(update)
        result = await word_check(update)

        return result

    finally:
        return {"ok": True}


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
