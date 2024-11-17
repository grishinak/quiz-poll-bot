from database.models import async_session
from database.models import User, Poll, Player, Answer
from sqlalchemy import select  # , update, delete


async def set_user(tg_id, first_name, last_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, first_name=first_name, last_name=last_name))
        await session.commit()
