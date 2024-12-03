from database.models import async_session
from database.models import User, Poll, Lobby, LobbyParticipant, Answer
from sqlalchemy import select, insert

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
    """
    Создает лобби с указанным poll_id и возвращает его ID.
    :param poll_id: ID опроса
    :param creator_id: ID создателя
    :return: ID созданного лобби
    """
    async with async_session() as session:
        async with session.begin():
            # Создаем запись о лобби
            stmt = (
                insert(Lobby)
                .values(poll_id=poll_id, creator_id=creator_id)
                .returning(Lobby.id)
            )
            result = await session.execute(stmt)
            lobby_id = result.scalar()
            return lobby_id


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


# add lobby_participant data to db from ???
async def set_lobby_participant(lobby_id: int, user_id: int):
    async with async_session() as session:
        lobby_participant = LobbyParticipant(lobby_id=lobby_id, user_id=user_id)
        session.add(lobby_participant)

        # Фиксируем изменения в базе данных
        await session.commit()


from sqlalchemy.future import select
from database.models import Poll


async def get_poll_by_id_and_creator(poll_id: int, creator_id: int):
    """
    Проверяет существование опроса с указанным ID и принадлежность создателю.
    :param poll_id: ID опроса
    :param creator_id: ID создателя
    :return: Объект Poll или None
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Poll).where(Poll.id == poll_id, Poll.creator_id == creator_id)
            )
            return result.scalar()


# Проверка существования лобби
async def check_lobby_exists(lobby_id: int):
    async with async_session() as session:
        stmt = select(Lobby).filter(Lobby.id == lobby_id)
        result = await session.execute(stmt)
        return result.scalars().first() is not None


# Проверка, является ли пользователь участником лобби
async def check_if_participant_exists(lobby_id: int, user_id: int):
    async with async_session() as session:
        stmt = select(LobbyParticipant).filter(
            LobbyParticipant.lobby_id == lobby_id, LobbyParticipant.user_id == user_id
        )
        result = await session.execute(stmt)
        return result.scalars().first() is not None


# Добавление участника в лобби
async def set_lobby_participant(lobby_id: int, user_id: int):
    async with async_session() as session:
        participant = LobbyParticipant(lobby_id=lobby_id, user_id=user_id)
        session.add(participant)
        await session.commit()
        return participant


async def get_poll_question(poll_id: int):
    async with async_session() as session:
        result = await session.execute(select(Poll).filter(Poll.id == poll_id))
        poll = result.scalars().first()
        if poll:
            return poll.question
        else:
            return None


# Получение участников лобби
async def get_lobby_participants(lobby_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(LobbyParticipant.user_id).filter(
                LobbyParticipant.lobby_id == lobby_id
            )
        )
        return [row.user_id for row in result.all()]


async def get_poll_id_for_lobby(lobby_id: int):
    async with async_session() as session:
        # Выполняем запрос для получения poll_id, связанного с lobby_id
        result = await session.execute(select(Lobby).filter(Lobby.id == lobby_id))
        lobby = result.scalars().first()  # Извлекаем первый результат или None

        # Проверяем, существует ли лобби и возвращаем poll_id
        if lobby:
            return lobby.poll_id
        else:
            return None


# Сохранение ответа пользователя
async def set_answer(lobby_id: int, participant_id: int, user_answer: str):
    """
    Сохраняет ответ пользователя в базе данных.

    :param lobby_id: ID лобби, связанного с ответом.
    :param participant_id: ID участника лобби.
    :param user_answer: Ответ пользователя.
    :return: Сохраненная запись ответа.
    """
    async with async_session() as session:
        answer = Answer(
            lobby_id=lobby_id, lobby_participant_id=participant_id, answer=user_answer
        )
        session.add(answer)
        await session.commit()
        return answer


from sqlalchemy.sql import text


async def get_lobby_data(creator_tg_id: int):
    query = text(
        """
    SELECT lobbies.id, lobby_participants.id, answers.answer,
    users.first_name,users.last_name, polls.name,polls.id
    FROM lobbies
    JOIN lobby_participants ON lobby_participants.lobby_id=lobbies.id
    JOIN answers ON lobby_participants.id=answers.id
    JOIN users ON users.tg_id=lobby_participants.user_id
    JOIN polls ON polls.id=lobbies.poll_id

    WHERE lobbies.creator_id = :creator_tg_id;
    """
    )

    async with async_session() as session:
        result = await session.execute(query, {"creator_tg_id": creator_tg_id})
        rows = result.fetchall()
        return [
            {
                "lobby_id": row[0],
                "participant_id": row[1],
                "answer": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "polls_name": row[5],
                "polls_id": row[6],
            }
            for row in rows
        ]


async def update_lobby_collecting_status(lobby_id: int, is_collecting: bool):
    async with async_session() as session:
        await session.execute(
            text(
                "UPDATE lobbies SET is_collecting = :is_collecting WHERE id = :lobby_id"
            ),
            {"is_collecting": is_collecting, "lobby_id": lobby_id},
        )
        await session.commit()


async def is_lobby_collecting(lobby_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            text("SELECT is_collecting FROM lobbies WHERE id = :lobby_id"),
            {"lobby_id": lobby_id},
        )
        row = result.scalar()
        return bool(row) if row is not None else False
