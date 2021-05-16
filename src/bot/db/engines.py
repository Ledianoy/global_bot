from sqlalchemy.ext.asyncio import create_async_engine

from bot.config import settings
from bot.db.util import with_driver

engine = create_async_engine(
    with_driver(settings.database_url, "asyncpg"),
    echo=True,
)
