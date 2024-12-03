from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database.requests as rq

router = Router()


@router.message(Command("polls_list"))
async def show_polls_list(message: Message):
    user_id = message.from_user.id  # ID пользователя Telegram

    # Получаем список опросов из базы данных
    polls = await rq.get_polls(user_id)

    # Если у пользователя нет созданных опросов
    if not polls:
        await message.answer("У вас нет созданных опросов.")

    else:
        # Формируем сообщение со списком опросов
        response = "Ваши созданные опросы:\n\n"
        for lobby_id, poll_id, creator_id in polls:
            response += f" - Опрос #{lobby_id} с вопросом #{poll_id}\n"

        # Отправляем пользователю список опросов
        await message.answer(response)
