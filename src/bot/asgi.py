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
from bot.send import get_webhook_info
from bot.send import set_webhook
from bot.telegram.types import Update
from bot.telegram.util import shadow_webhook_secret
from bot.util import debug
from bot.way import process_way
from bot.way_chenal import api_chenel
from bot.way_chenal import repost_chanel
from bot.way_word import word_check

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
        await api_chenel(update)
        if update.message.chat.type == "private":
            result = await process_way(update)
        if update.message.forward_from_chat is not None:
            result = await repost_chanel(update)
        result = await word_check(update)

        return result

    finally:
        return {"ok": True}
