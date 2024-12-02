from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.requests import get_lobby_data

router = Router()


@router.message(Command("show_answers"))
async def show_lobby_users(message: Message):

    user_id = message.from_user.id  # ID пользователя Telegram

    # Получаем данные о лобби, участниках и их ответах
    lobby_data = await get_lobby_data(user_id)

    if not lobby_data:
        await message.answer("У вас нет лобби с участниками.")
        return

    # Формируем сообщение с данными
    response = "Ваши лобби и ответы участников:\n\n"
    current_lobby_id = None

    for data in lobby_data:
        if data["lobby_id"] != current_lobby_id:
            current_lobby_id = data["lobby_id"]
            response += f"🔹 Лобби #{current_lobby_id} (Опрос #{data['polls_id']}, Название:'{data['polls_name']})':\n"

        response += f"👤 {data['first_name']} {data['last_name']}: {data['answer']}\n"
    # print(data) #logging info
    await message.answer(response)
