from database.models import async_session
from database.models import User, Poll, Lobby
from sqlalchemy import select

# func for setting user data from /start
async def set_user(tg_id, first_name=None, last_name=None):
    async with async_session() as session:
        # Получаем пользователя из базы данных
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            # Если пользователь отсутствует, добавляем нового
            user = User(
                tg_id=tg_id,
                first_name=first_name or "",  # Если None, сохраняем пустую строку
                last_name=last_name or "",  # Если None, сохраняем пустую строку
            )
            session.add(user)
        else:
            # Если пользователь существует, обновляем его данные
            if first_name:  # Проверяем, что передано имя
                user.first_name = first_name
            if last_name:  # Проверяем, что передана фамилия
                user.last_name = last_name

        # Фиксируем изменения в базе данных
        await session.commit()


# add poll data to db from check_true in create_poll fsm
async def set_poll(name: str, question: str, answer: str, creator_id: int):
    async with async_session() as session:
        poll = Poll(name=name, question=question, answer=answer, creator_id=creator_id)
        session.add(poll)

        # Фиксируем изменения в базе данных
        await session.commit()


async def get_polls(user_id: int):
    """
    Получает список опросов, созданных пользователем.

    :param user_id: ID пользователя Telegram
    :return: Список словарей с данными опросов
    """
    async with async_session() as session:
        async with session.begin():
            # Выбираем только необходимые данные, чтобы избежать привязки к сессии
            result = await session.execute(
                select(Poll.id, Poll.name, Poll.question, Poll.answer).where(
                    Poll.creator_id == user_id
                )
            )
            # Возвращаем список кортежей, который можно использовать вне сессии
            return result.all()


# TODO: delete users polls from db from user menu


# add lobby data to db from ???
async def set_lobby(poll_id: int, creator_id: int):
    async with async_session() as session:
        lobby = Lobby(poll_id=poll_id, creator_id=creator_id)
        session.add(lobby)

        # Фиксируем изменения в базе данных
        await session.commit()


async def get_lobbies(user_id: int):
    """
    Получает список лобби, созданных пользователем.

    :param user_id: ID пользователя Telegram
    :return: Список словарей с данными лобби
    """
    async with async_session() as session:
        async with session.begin():
            # Выбираем только необходимые данные, чтобы избежать привязки к сессии
            result = await session.execute(
                select(Lobby.id, Lobby.poll_id, Lobby.creator_id).where(
                    Lobby.creator_id == user_id
                )
            )
            # Возвращаем список кортежей, который можно использовать вне сессии
            return result.all()
