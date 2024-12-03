from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import database.requests as rq
import keyboards.questions_list as kb

router = Router()


@router.message(Command("questions_list"))
async def show_poll_list_cmd(message: Message):
    user_id = message.from_user.id  # ID пользователя Telegram

    # Получаем список  Вопросов из базы данных
    questions = await rq.get_questions(user_id)

    # Если у пользователя нет созданных вопросов
    if not questions:
        await message.answer("У вас нет созданных вопросов.")

    else:
        # Формируем сообщение со списком опросов
        response = "Ваши созданные вопросы:\n\n"
        for poll_id, poll_name, poll_question, poll_answer in questions:
            response += (
                f"📝 Вопрос #{poll_id}: {poll_question}\n\tОтвет: {poll_answer}\n\n"
            )

        # Отправляем пользователю список опросов
        await message.answer(response)


@router.callback_query(F.data == "questions_list")
async def show_poll_list_clb(callback: CallbackQuery):
    callback.answer("Список вопросов.")
    user_id = callback.from_user.id  # ID пользователя Telegram

    # Получаем список опросов из базы данных
    questions = await rq.get_questions(user_id)

    # Если у пользователя нет созданных опросов
    if not questions:
        await callback.message.answer("У вас нет созданных вопросов.")

    else:
        # Формируем сообщение со списком опросов
        response = "Ваши созданные вопросы:\n\n"
        for poll_id, poll_name, poll_question, poll_answer in questions:
            response += (
                f"📝 Вопрос #{poll_id}: {poll_question}\n\tОтвет: {poll_answer}\n\n"
            )

        # Отправляем пользователю список опросов
        await callback.message.answer(response, reply_markup=kb.create_poll)
