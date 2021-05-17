import os
from unittest import mock

import pytest

from bot.config import Settings


@pytest.mark.asyncio
def test_settings():
    new_env = {
        "ADMIN_PASSWORD": "admin_password",
        "BOT_TOKEN": "bot_token",
        "DATABASE_URL": "database_url",
        "INDEX_PATH" : "index_path",
        "PYTHONPATH": "python_path",
        "SERVICE_URL": "service_url",
        "WEBHOOK_SECRET": "webhook_secret",
    }



    with mock.patch.dict(os.environ, new_env, clear=True):
        settings = Settings()

    assert settings.admin_password == "admin_password"
    assert settings.bot_token == "bot_token"
    assert settings.database_url == "database_url"
    assert settings.index_path == "index_path"
    assert settings.python_path == "python_path"
    assert settings.service_url == "service_url"
    assert settings.webhook_secret == "webhook_secret"