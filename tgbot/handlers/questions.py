from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database.requests as rq
import keyboards.questions as kb


router = Router()


# /question handler
@router.message(Command("questions"))
async def cmd_help(message: Message):
    await message.answer(
        "Что вы хотите сделать с вопросами?", reply_markup=kb.questions_menu
    )


# class with fsm states
class CreateQuestion(StatesGroup):
    question = State()
    answer = State()


# Обработка нажатия кнопки (from start) и переход в состояние
@router.callback_query(F.data == "create_question")
async def process_create_poll_clb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали создание вопроса")  # alert
    await callback.message.answer("Вы начали создание вопроса!")  # message in chat

    # await state.set_state(CreateQuestion.name)  # goes to state
    # await callback.message.answer("Введите название вопроса:")

    await state.set_state(CreateQuestion.question)  # goes to state
    await callback.message.answer("Введите вопрос:")


@router.message(CreateQuestion.question)
async def process_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(CreateQuestion.answer)
    await message.answer(
        "Введите ожидаемый вами правильный ответ на свой вопрос (для результатов после опроса).:"
    )


@router.message(CreateQuestion.answer)
async def process_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()  # get all data about polls from user
    await message.answer(
        # f"Все ли верно?\n\nНазвание опроса: {data['name']}\nВопрос: {data['question']}\nОтвет: {data['answer']}",
        f"Все ли верно?\n\nВопрос: {data['question']}\nОжидаемый ответ: {data['answer']}",
        reply_markup=kb.check_menu,  # buttons for check
    )


# Обработка нажатия кнопки (from answer) и переход в состояние
@router.callback_query(F.data == "check_false")
async def process_check_false(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Данные не верны.")
    await callback.answer("Сначала")  # alert
    await callback.message.answer(
        "Вы начали создание вопроса сначала!"
    )  # message in chat

    # await state.set_state(CreateQuestion.name)  # goes to state
    # await callback.message.answer("Введите название опроса:")
    await state.set_state(CreateQuestion.question)  # goes to state
    await callback.message.answer("Введите вопрос:")


# Обработка нажатия кнопки (from answer) и переход в состояние
@router.callback_query(F.data == "check_true")
async def process_check_true(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Успешно")  # alert
    await callback.message.edit_text("Данные верны.")
    data = await state.get_data()

    creator_tg_id = callback.from_user.id
    try:
        # Сохраняем опрос в базе данных
        question_id = await rq.set_question(
            question=data["question"],
            answer=data["answer"],
            creator_tg_id=creator_tg_id,
        )

        # Отправляем сообщение пользователю о том, что опрос сохранен
        await callback.message.answer(f"Данные вопроса сохранены!")
        await callback.message.answer(
            f"Вопрос '{data['question']}' успешно создан.",
            reply_markup=kb.questions_list,
        )

    except Exception as e:
        # Если произошла ошибка, информируем пользователя
        await callback.message.answer(
            "Произошла ошибка при сохранении вопроса. Попробуйте снова."
        )
        print(f"Ошибка при сохранении вопроса: {e}")

    await state.clear()


@router.callback_query(F.data == "questions_list")
async def show_poll_list_clb(callback: CallbackQuery):
    callback.answer("Список вопросов.")
    user_id = callback.from_user.id  # ID пользователя Telegram

    # Получаем список опросов из базы данных
    questions = await rq.get_questions(user_id)

    # Если у пользователя нет созданных вопросов
    if not questions:
        await callback.message.answer("У вас нет созданных вопросов.")

    else:
        # Формируем сообщение со списком вопросов
        response = "Ваши созданные вопросы:\n\n"
        for question_id, poll_question, poll_answer in questions:
            response += (
                f"📝 Вопрос #{question_id}: {poll_question}\n\tОтвет: {poll_answer}\n\n"
            )

        # Отправляем пользователю список вопросов
        await callback.message.answer(response, reply_markup=kb.create_poll)
