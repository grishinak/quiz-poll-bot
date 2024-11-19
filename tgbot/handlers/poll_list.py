from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database.requests as rq

router = Router()


@router.message(Command("poll_list"))
async def show_poll_list(message: Message):
    user_id = message.from_user.id  # ID пользователя Telegram

    # Получаем список опросов из базы данных
    polls = await rq.get_polls(user_id)

    # Если у пользователя нет созданных опросов
    if not polls:
        await message.answer("У вас нет созданных опросов.")
        return

    # Формируем сообщение со списком опросов
    response = "Ваши созданные опросы:\n\n"
    for poll_id, poll_name, poll_question, poll_answer in polls:
        response += f"📝 Опрос #{poll_id}: {poll_name}\n\tВопрос: {poll_question}\n\tОтвет: {poll_answer}\n\n"

    # Отправляем пользователю список опросов
    await message.answer(response)
