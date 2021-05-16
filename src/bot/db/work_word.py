import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from .models import Word
from .session import begin_session


async def word_check_bd(text: str):
    word_bloc = False
    stmt = sa.select(Word).where(
        Word.zap_word == text,
    )
    async with begin_session() as session:
        response = await session.execute(stmt)
        temp: Word = response.scalars().first()
        if temp != None:
            if temp.zap_word == text:
                word_bloc = True

    return word_bloc


async def new_word(
    text: str,
) -> None:
    stmt = (
        insert(Word)
        .values(
            {
                Word.zap_word: text,
            }
        )
        .on_conflict_do_nothing(
            index_elements=["id"],
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)
