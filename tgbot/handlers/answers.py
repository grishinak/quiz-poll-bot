from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.models import async_session

import keyboards.answers as kb
import database.requests as rq

router = Router()


@router.message(Command("answers"))
async def show_poll_users(message: Message):
    await message.answer(
        "Выберите, откуда вы хотите получить ответы участников в ваших опросах:",
        reply_markup=kb.answers_menu,
    )


@router.callback_query(F.data == "answers")
async def show_lobby_users_clb(callback: CallbackQuery):
    callback.answer("Вы получаете список ответов")
    user_id = callback.from_user.id  # ID пользователя Telegram

    # Получаем данные о лобби, участниках и их ответах
    poll_data = await rq.get_poll_data(user_id)

    if not poll_data:
        await callback.message.answer("У вас нет опросов с ответами участников.")
        return

    # Формируем сообщение с данными
    response = " Ответы участников в ваших опросах:\n\n"
    current_poll_id = None

    for data in poll_data:
        if data["lobby_id"] != current_poll_id:
            current_poll_id = data["lobby_id"]
            response += f"🚪 Опрос #{current_poll_id} (Вопрос #{data['polls_id']}, '{data['question']}'):\n"

        response += (
            f"\t\t 👤 {data['first_name']} {data['last_name']}: {data['answer']}\n"
        )
    # print(data) #logging info
    await callback.message.answer(response)


@router.callback_query(F.data == "ans")
async def show_last_lobby_users_clb(callback: CallbackQuery):
    await callback.answer("Вы получаете список ответов для последнего опроса")
    user_id = callback.from_user.id  # ID пользователя Telegram

    # Получаем данные о лобби, участниках и их ответах
    async with async_session() as session:
        poll_data = await rq.get_last_poll_answers(session, creator_tg_id=user_id)

    if not poll_data:
        await callback.message.answer("Вы еще не проводили опросов.")
        return

    # Формируем сообщение с данными
    response = "Ответы участников в вашем последнем опросе:\n\n"

    for data in poll_data:
        response += f"👤 {data['first_name']} {data['last_name']}: {data['answer']}\n"

    await callback.message.answer(response)
