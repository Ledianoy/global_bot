import pytest
from dotenv import load_dotenv
from starlette import status

from bot.config import settings

load_dotenv()


@pytest.mark.asyncio
async def test(http_session):
    service = settings.service_url
    assert service

    url_settings = f"{service}/settings/"

    async with http_session.get(url_settings) as resp:
        assert resp.status == status.HTTP_404_NOT_FOUND