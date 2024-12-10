from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.requests import get_poll_data, get_last_poll_data, get_name_by_id

import keyboards.answers as kb

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
    poll_data = await get_poll_data(user_id)

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


# output for just taken poll
from aiogram.types import CallbackQuery


@router.callback_query(F.data == "ans")
async def show_last_lobby_users_clb(callback: CallbackQuery):
    await callback.answer(
        "Вы получаете список ответов для последнего опроса"
    )  # Ответ пользователю

    user_id = callback.from_user.id  # ID пользователя Telegram
    poll_info = await get_last_poll_data(user_id)

    if not poll_info:
        await callback.message.answer("Вы еще не проводили опросов.")
        return

    poll_id = poll_info["poll_id"]
    poll_data = poll_info["poll_data"]

    if not poll_data:
        await callback.message.answer("У последнего опроса нет ответов.")
        return

    # Формирование ответа
    response = (
        f"Ответы участников в вашем последнем опросе:\n\n" f"🚪 Опрос #{poll_id}\n"
    )

    for data in poll_data:
        tg_id = data[1]  # Получаем ID пользователя
        full_name = await get_name_by_id(tg_id)
        print(full_name)
        response += f"\t\t👤 {full_name[0]} {full_name[1]}: {data[2]}\n"

    # Отправка ответа
    await callback.message.answer(response)
