from database.models import async_session
from database.models import User
from sqlalchemy import select


async def set_user(tg_id, first_name, last_name):
    async with async_session() as session:
        # Получаем пользователя из базы данных
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            # Если пользователь отсутствует, добавляем нового
            user = User(tg_id=tg_id, first_name=first_name, last_name=last_name)
            session.add(user)
        else:
            # Если пользователь существует, обновляем его данные
            user.first_name = first_name
            user.last_name = last_name

        # Фиксируем изменения в базе данных
        await session.commit()
