from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database.requests as rq

router = Router()


@router.message(Command("lobbies_list"))
async def show_lobbies_list(message: Message):
    user_id = message.from_user.id  # ID пользователя Telegram

    # Получаем список опросов из базы данных
    lobbies = await rq.get_lobbies(user_id)

    # Если у пользователя нет созданных опросов
    if not lobbies:
        await message.answer("У вас нет созданных лобби.")

    else:
        # Формируем сообщение со списком опросов
        response = "Ваши созданные лобби:\n\n"
        for lobby_id, poll_id, creator_id in lobbies:
            response += f" - Лобби #{lobby_id} с опросом #{poll_id}\n"

        # Отправляем пользователю список опросов
        await message.answer(response)
