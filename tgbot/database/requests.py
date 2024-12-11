from database.models import async_session
from database.models import User, Question, Poll, PollParticipant, Answer
from sqlalchemy import select, insert, update, delete, BigInteger, desc, asc


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


# add polls data to db from check_true in create_question fsm
async def set_question(question: str, answer: str, creator_tg_id: int):
    async with async_session() as session:
        polls = Question(question=question, answer=answer, creator_tg_id=creator_tg_id)
        session.add(polls)

        # Фиксируем изменения в базе данных
        await session.commit()


async def get_questions(user_id: int):
    """
    Получает список опросов, созданных пользователем.

    :param user_id: ID пользователя Telegram
    :return: Список словарей с данными опросов
    """
    async with async_session() as session:
        async with session.begin():
            # Выбираем только необходимые данные, чтобы избежать привязки к сессии
            result = await session.execute(
                select(Question.id, Question.question, Question.answer).where(
                    Question.creator_tg_id == user_id
                )
            )
            # Возвращаем список кортежей, который можно использовать вне сессии
            return result.all()


# TODO: delete users questions from db from user menu


# add lobby data to db from ???


async def set_poll(question_id: int, creator_tg_id: int):
    """
    Создает опрос с указанным question_id и возвращает его ID.
    :param question_id: ID опроса
    :param creator_tg_id: ID создателя
    :return: ID созданного опроса
    """
    async with async_session() as session:
        async with session.begin():
            # Создаем запись о лобби
            stmt = (
                insert(Poll)
                .values(question_id=question_id, creator_tg_id=creator_tg_id)
                .returning(Poll.id)
            )
            result = await session.execute(stmt)
            poll_id = result.scalar()
            return poll_id


async def get_polls(user_id: int):
    """
    Получает список опросов, созданных пользователем.

    :param user_id: ID пользователя Telegram
    :return: Список словарей с данными лобби
    """
    async with async_session() as session:
        async with session.begin():
            # Выбираем только необходимые данные, чтобы избежать привязки к сессии
            result = await session.execute(
                select(Poll.id, Poll.question_id, Poll.creator_tg_id).where(
                    Poll.creator_tg_id == user_id
                )
            )
            # Возвращаем список кортежей, который можно использовать вне сессии
            return result.all()


# add lobby_participant data to db from ???
async def set_poll_participant(poll_id: int, user_tg_id: BigInteger):
    async with async_session() as session:
        lobby_participant = PollParticipant(poll_id=poll_id, user_tg_id=user_tg_id)
        session.add(lobby_participant)

        # Фиксируем изменения в базе данных
        await session.commit()


async def get_poll_by_id_and_creator(question_id: int, creator_tg_id: int):
    """
    Получает вопрос с указанным ID и создателем.
    :param question_id: ID вопроса
    :param creator_tg_id: ID создателя
    :return: Объект Question или None
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Question).where(
                    Question.id == question_id, Question.creator_tg_id == creator_tg_id
                )
            )
            return result.scalar()


# Проверка существования опроса
async def check_poll_exists(poll_id: int):
    async with async_session() as session:
        stmt = select(Poll).filter(Poll.id == poll_id)
        result = await session.execute(stmt)
        return result.scalars().first() is not None


# Проверка, является ли пользователь участником опроса
async def check_if_participant_exists(poll_id: int, user_tg_id: BigInteger):
    async with async_session() as session:
        stmt = select(PollParticipant).filter(
            PollParticipant.poll_id == poll_id,
            PollParticipant.user_tg_id == user_tg_id,
        )
        result = await session.execute(stmt)
        return result.scalars().first() is not None


# Добавление участника в опрос
async def set_poll_participant(poll_id: int, user_tg_id: int):
    async with async_session() as session:
        participant = PollParticipant(poll_id=poll_id, user_tg_id=user_tg_id)
        session.add(participant)
        await session.commit()
        return participant


async def get_poll_question_with_id(question_id: int):
    async with async_session() as session:
        poll_query = (
            select(Question.question, Question.id)
            .join(Poll, Poll.question_id == Question.id)
            .where(Poll.id == question_id)
        )
        result = await session.execute(poll_query)
        question_data = result.first()
        return question_data


async def get_poll_question(question_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Question).filter(Question.id == question_id)
        )
        polls = result.scalars().first()
        if polls:
            return polls.question
        else:
            return None


# Получение участников опроса
async def get_poll_participants(poll_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(PollParticipant.user_tg_id).filter(
                PollParticipant.poll_id == poll_id
            )
        )
        return [row.user_tg_id for row in result.all()]


async def get_poll_id_for_lobby(poll_id: int):
    async with async_session() as session:
        # Выполняем запрос для получения question_id, связанного с poll_id
        result = await session.execute(select(Poll).filter(Poll.id == poll_id))
        lobby = result.scalars().first()  # Извлекаем первый результат или None

        # Проверяем, существует ли опрос и возвращаем question_id
        if lobby:
            return lobby.question_id
        else:
            return None


# Сохранение ответа пользователя
async def set_answer(poll_id: int, participant_id: int, user_answer: str):
    """
    Сохраняет ответ пользователя в базе данных.

    :param poll_id: ID опроса, связанного с ответом.
    :param participant_id: ID участника опроса.
    :param user_answer: Ответ пользователя.
    :return: Сохраненная запись ответа.
    """
    async with async_session() as session:
        answer = Answer(
            poll_id=poll_id, lobby_participant_id=participant_id, answer=user_answer
        )
        session.add(answer)
        await session.commit()
        return answer


async def get_poll_data(creator_tg_id: int):
    async with async_session() as session:
        # Создаем запрос с использованием ORM
        result = await session.execute(
            select(
                Poll.id.label("poll_id"),
                PollParticipant.id.label("participant_id"),
                Answer.answer.label("answer"),
                User.first_name.label("first_name"),
                User.last_name.label("last_name"),
                Question.id.label("polls_id"),
                Question.question.label("question"),
            )
            .join(PollParticipant, PollParticipant.poll_id == Poll.id)
            .join(Answer, Answer.id == PollParticipant.id)
            .join(User, User.tg_id == PollParticipant.user_tg_id)
            .join(Question, Question.id == Poll.question_id)
            .where(Poll.creator_tg_id == creator_tg_id)
        )

        # Преобразуем результат в список словарей
        rows = result.all()
        return [
            {
                "poll_id": row.poll_id,
                "participant_id": row.participant_id,
                "answer": row.answer,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "polls_id": row.polls_id,
                "question": row.question,
            }
            for row in rows
        ]


async def update_poll_collecting_status(poll_id: int, is_collecting: bool):
    async with async_session() as session:
        # Создаем запрос на обновление
        await session.execute(
            update(Poll).where(Poll.id == poll_id).values(is_collecting=is_collecting)
        )
        # Фиксируем изменения
        await session.commit()


async def is_poll_collecting(poll_id: int) -> bool:
    async with async_session() as session:
        # Создаем запрос на выборку
        result = await session.execute(
            select(Poll.is_collecting).where(Poll.id == poll_id)
        )
        # Извлекаем значение
        row = result.scalar()
        return bool(row) if row is not None else False


async def delete_user_polls_and_questions(user_tg_id: int):
    async with async_session() as session:
        # Найти пользователя
        user = await session.execute(select(User).where(User.tg_id == user_tg_id))
        user = user.scalar_one_or_none()

        if not user:
            return  # Пользователь не найден, нечего удалять.

        # Найти вопросы, созданные пользователем
        questions = await session.execute(
            select(Question).where(
                Question.creator_tg_id == user.tg_id
            )  # Используем user.id
        )
        questions = questions.scalars().all()

        # Найти опросы, созданные пользователем
        polls = await session.execute(
            select(Poll).where(Poll.creator_tg_id == user.tg_id)  # Используем user.id
        )
        polls = polls.scalars().all()

        # Найти и удалить ответы, связанные с опросами пользователя
        poll_ids = [poll.id for poll in polls]
        if poll_ids:
            await session.execute(delete(Answer).where(Answer.poll_id.in_(poll_ids)))

            # Удалить участников, связанные с опросами пользователя
            await session.execute(
                delete(PollParticipant).where(PollParticipant.poll_id.in_(poll_ids))
            )

        # Удалить опросы
        for poll in polls:
            await session.delete(poll)

        # Удалить вопросы
        for question in questions:
            await session.delete(question)

        await session.commit()


async def get_poll_creator_id(poll_id: int) -> int | None:
    async with async_session() as session:
        result = await session.execute(
            select(Poll.creator_tg_id).where(Poll.id == poll_id)
        )
        return result.scalar_one_or_none()


async def get_last_poll_data(user_id: int):
    """
    Получает данные о последнем опросе и ответах участников для заданного пользователя.

    :param user_id: ID пользователя Telegram, создавшего опрос.
    :return: Словарь с данными о последнем опросе или None, если данных нет.
    """
    async with async_session() as session:
        # Получение ID последнего опроса
        last_poll_query = (
            select(Poll.id)
            .where(Poll.creator_tg_id == user_id)
            .order_by(desc(Poll.id))  # Упорядочиваем в обратном порядке по ID
            .limit(1)
        )
        last_poll_result = await session.execute(last_poll_query)
        last_poll_id = last_poll_result.scalar_one_or_none()
        print(f"last_poll_result:{last_poll_result}")
        print(f"last_poll_id:{last_poll_id}")
        if not last_poll_id:
            return None

        # Получение данных об участниках и их ответах
        poll_data_query = (
            select(
                Poll.id,
                Answer.lobby_participant_id,
                Answer.answer,
            )
            .join(Answer, Poll.id == Answer.poll_id)
            .where(Poll.id == last_poll_id)
        )
        poll_data_result = await session.execute(poll_data_query)
        poll_data = poll_data_result.all()
        print(f"poll_data:{poll_data}")
        return {"poll_id": last_poll_id, "poll_data": poll_data}


async def get_name_by_id(tg_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User.first_name, User.last_name).where(User.tg_id == tg_id)
        )
        user = result.fetchone()  # Возвращает строку или None
        if user:
            return user.first_name, user.last_name
        return None, None  # Возвращаем пустые значения, если пользователь не найден


async def get_all_poll_data(user_id: int):
    """
    Получает данные о всех опросах и ответах участников для заданного пользователя.

    :param user_id: ID пользователя Telegram, создавшего опрос.
    :return: Словарь с данными о последнем опросе или None, если данных нет.
    """
    async with async_session() as session:
        # Получение ID последнего опроса
        all_poll_query = (
            select(Poll.id)
            .where(Poll.creator_tg_id == user_id)
            .order_by(asc(Poll.id))  # Упорядочиваем в прямом порядке
        )
        all_poll_result = await session.execute(all_poll_query)
        all_poll_id = all_poll_result.scalars().all()
        print(f"all_poll_result:{all_poll_result}")  # log
        print(f"all_poll_id:{all_poll_id}")  # log
        if not all_poll_id:
            return None

        # Получение данных об участниках и их ответах
        poll_data_query = (
            select(
                Poll.id,
                Answer.lobby_participant_id,
                Answer.answer,
            )
            .join(Answer, Poll.id == Answer.poll_id)
            .where(Poll.id.in_(all_poll_id))
        )
        poll_data_result = await session.execute(poll_data_query)
        poll_data = poll_data_result.all()
        print(f"poll_data:{poll_data}")  # log
        return {"poll_id": all_poll_id, "poll_data": poll_data}
