from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import database.requests as rq

import keyboards.answers as kb

router = Router()


@router.message(Command("answers"))
async def show_poll_users(message: Message):
    await message.answer(
        "Выберите, откуда вы хотите получить ответы участников в ваших опросах:",
        reply_markup=kb.answers_menu,
    )


@router.callback_query(F.data == "answers")
async def show_all_lobby_users_clb(callback: CallbackQuery):
    await callback.answer("Вы получаете список ответов для всех ваших опросов.")

    user_id = callback.from_user.id  # ID пользователя Telegram
    poll_info = await rq.get_all_poll_data(user_id)

    if not poll_info:
        await callback.message.answer("Вы еще не проводили опросов.")
        return

    all_poll_ids = poll_info["poll_id"]
    poll_data = poll_info["poll_data"]

    if not poll_data:
        await callback.message.answer("У ваших опросов нет ответов.")
        return

    # Формирование ответа
    response = "Ответы участников во всех ваших опросах:\n\n"
    current_poll_id = None

    for data in poll_data:
        poll_id = data[0]
        tg_id = data[1]
        answer = data[2]
        question = await rq.get_poll_question_with_id(poll_id)

        # Если новый опрос, добавляем заголовок
        if poll_id != current_poll_id:
            current_poll_id = poll_id
            response += f"\n🚪 Опрос #{poll_id}: {question[0]}. Вопрос #{question[1]} '{question[0]}' \n"

        # Получение имени участника
        full_name = await rq.get_name_by_id(tg_id)
        if full_name:
            response += f"\t\t👤 {full_name[0]} {full_name[1]}: {answer}\n"
        else:
            response += f"\t\t👤 Пользователь с ID {tg_id}: {answer}\n"

    # Отправка ответа
    await callback.message.answer(response)


@router.callback_query(F.data == "ans")
async def show_last_lobby_users_clb(callback: CallbackQuery):
    await callback.answer(
        "Вы получаете список ответов для последнего опроса"
    )  # Ответ пользователю

    user_id = callback.from_user.id  # ID пользователя Telegram
    poll_info = await rq.get_last_poll_data(user_id)

    if not poll_info:
        await callback.message.answer("Вы еще не проводили опросов.")
        return

    poll_id = poll_info["poll_id"]
    poll_data = poll_info["poll_data"]

    if not poll_data:
        await callback.message.answer("У последнего опроса нет ответов.")
        return

    question = await rq.get_poll_question_with_id(poll_id)
    # Формирование ответа
    response = (
        f"Ответы участников в вашем последнем опросе:\n\n"
        f"🚪 Опрос #{poll_id}. Вопрос #{question[1]} '{question[0]}'\n"
    )

    for data in poll_data:
        tg_id = data[1]  # Получаем ID пользователя
        full_name = await rq.get_name_by_id(tg_id)
        print(full_name)
        response += f"\t\t👤 {full_name[0]} {full_name[1]}: {data[2]}\n"

    # Отправка ответа
    await callback.message.answer(response)
