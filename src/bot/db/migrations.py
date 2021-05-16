import asyncio

import sqlalchemy as sa

from bot.db.engines import engine

migrations_reports = [
    """
        create table if not exists repost_chenal(
        id serial primary key,
        id_chenal bigint unique,
        chenel_name text
        );
    """,
]
migrations_user = [
    """
        create table if not exists users(
        id serial primary key,
        user_id integer unique,
        state_auth integer,
        number_post bigint unique
        );
    """,
]

migrations_words = [
    """
        create table if not exists words(
        id serial primary key,
        zap_word text
        );
    """,
]


async def apply_migrations():
    async with engine.begin() as conn:
        for migration in migrations_reports:
            await conn.execute(sa.text(migration))
    async with engine.begin() as conn:
        for migration in migrations_user:
            await conn.execute(sa.text(migration))
    async with engine.begin() as conn:
        for migration in migrations_words:
            await conn.execute(sa.text(migration))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(apply_migrations())
