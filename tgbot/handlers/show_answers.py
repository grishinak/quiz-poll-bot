from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.requests import get_lobby_data

router = Router()


@router.message(Command("show_answers"))
async def show_lobby_users(message: Message):

    user_id = message.from_user.id  # ID пользователя Telegram

    # Получаем данные о лобби, участниках и их ответах
    lobby_data = await get_lobby_data(user_id)

    if not lobby_data:
        await message.answer("У вас нет опросов с участниками.")
        return

    # Формируем сообщение с данными
    response = " Ответы участников в ваших опросах:\n\n"
    current_lobby_id = None

    for data in lobby_data:
        if data["lobby_id"] != current_lobby_id:
            current_lobby_id = data["lobby_id"]
            response += f"🚪 Лобби #{current_lobby_id} (Опрос #{data['polls_id']}, Название:'{data['question']})':\n"

        response += (
            f"\t\t 👤 {data['first_name']} {data['last_name']}: {data['answer']}\n"
        )
    # print(data) #logging info
    await message.answer(response)


@router.callback_query(F.data == "show_answers")
async def show_lobby_users_clb(callback: CallbackQuery):
    callback.answer("Вы получаете список ответов")
    user_id = callback.from_user.id  # ID пользователя Telegram

    # Получаем данные о лобби, участниках и их ответах
    lobby_data = await get_lobby_data(user_id)

    if not lobby_data:
        await callback.message.answer("У вас нет опросов с участниками.")
        return

    # Формируем сообщение с данными
    response = " Ответы участников в ваших опросах:\n\n"
    current_lobby_id = None

    for data in lobby_data:
        if data["lobby_id"] != current_lobby_id:
            current_lobby_id = data["lobby_id"]
            response += f"🚪 Опрос #{current_lobby_id} (Вопрос #{data['polls_id']}, '{data['question']}'):\n"

        response += (
            f"\t\t 👤 {data['first_name']} {data['last_name']}: {data['answer']}\n"
        )
    # print(data) #logging info
    await callback.message.answer(response)
