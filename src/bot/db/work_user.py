from typing import Any
from typing import Dict
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from .models import User
from .session import begin_session


async def init_user(user_id: int) -> None:
    stmt = (
        insert(User)
        .values(
            {
                User.user_id: user_id,
            }
        )
        .on_conflict_do_nothing(
            index_elements=["user_id"],
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def get_user(user_id: int) -> Optional[User]:
    stmt = sa.select(User).where(
        User.user_id == user_id,
    )

    async with begin_session() as session:
        response = await session.execute(stmt)
        user: User = response.scalars().first()

    return user


async def reset_user_auth_data(user_id: int) -> None:
    values = {
        User.blog_user_id: None,
        User.blog_username: None,
        User.state_auth: None,
    }

    await _update_user(user_id, values)


async def set_user_auth_state(
    user_id: int,
    state: int,
) -> None:
    values = {
        User.state_auth: state,
    }

    await _update_user(user_id, values)


async def _update_user(
    user_id: int,
    values: Dict[str, Any],
) -> None:
    stmt = (
        sa.update(User)
        .where(
            User.user_id == user_id,
        )
        .values(values)
    )

    async with begin_session() as session:
        await session.execute(stmt)
