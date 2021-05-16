from typing import Any
from typing import Dict

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from .models import Chenal
from .session import begin_session


async def id_chenal(id: int, name: str):
    stmt = sa.select(Chenal).where(
        Chenal.id_chenal == id,
    )
    chenal_bloc = False
    async with begin_session() as session:
        response = await session.execute(stmt)
        post: Chenal = response.scalars().first()
    if post.id_chenal == id:
        chenal_bloc = True
        if post.chenel_name != name:
            values = {
                Chenal.chenel_name: name,
            }
            await _update_name(id, values)
    return chenal_bloc


async def _update_name(
    id: int,
    values: Dict[str, Any],
) -> None:
    stmt = (
        sa.update(Chenal)
        .where(
            Chenal.id_chenal == id,
        )
        .values(values)
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def new_chenal(
    id: int,
    name: str,
) -> None:
    stmt = (
        insert(Chenal)
        .values(
            {
                Chenal.id_chenal: id,
                Chenal.chenel_name: name,
            }
        )
        .on_conflict_do_nothing(
            index_elements=["id_chenal"],
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)
