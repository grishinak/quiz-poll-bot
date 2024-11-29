from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database.requests as rq
import keyboards.create_poll as kb

router = Router()

# class with fsm states
class CreatePoll(StatesGroup):
    name = State()
    question = State()
    answer = State()


# Обработка нажатия кнопки (from start) и переход в состояние
@router.callback_query(F.data == "create_poll")
async def process_create_poll_clb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали создание опроса")  # alert
    await callback.message.answer("Вы начали создание опроса!")  # message in chat

    await state.set_state(CreatePoll.name)  # goes to state
    await callback.message.answer("Введите название опроса:")


# Обработка команды и переход в состояние
@router.message(Command("create_poll"))
async def process_create_poll_cmd(message: Message, state: FSMContext):
    await message.answer("Вы начали создание опроса!")  # message in chat

    await state.set_state(CreatePoll.name)  # goes to state
    await message.answer("Введите название опроса:")


@router.message(CreatePoll.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreatePoll.question)
    await message.answer("Введите вопрос:")


@router.message(CreatePoll.question)
async def process_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(CreatePoll.answer)
    await message.answer("Введите ответ на свой вопрос (для результатов после опроса):")


@router.message(CreatePoll.answer)
async def process_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()  # get all data about poll from user
    await message.answer(
        f"Все ли верно?\n\nНазвание опроса: {data['name']}\nВопрос: {data['question']}\nОтвет: {data['answer']}",
        reply_markup=kb.check_menu,  # buttons for check
    )


# Обработка нажатия кнопки (from answer) и переход в состояние
@router.callback_query(F.data == "check_false")
async def process_check_false(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Данные не верны.")
    await callback.answer("Сначала")  # alert
    await callback.message.answer(
        "Вы начали создание опроса сначала!"
    )  # message in chat

    await state.set_state(CreatePoll.name)  # goes to state
    await callback.message.answer("Введите название опроса:")


# Обработка нажатия кнопки (from answer) и переход в состояние
@router.callback_query(F.data == "check_true")
async def process_check_true(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Успешно")  # alert
    await callback.message.edit_text("Данные верны.")
    data = await state.get_data()

    creator_id = callback.from_user.id
    try:
        # Сохраняем опрос в базе данных
        poll_id = await rq.set_poll(
            name=data["name"],
            question=data["question"],
            answer=data["answer"],
            creator_id=creator_id,
        )

        # Отправляем сообщение пользователю о том, что опрос сохранен
        await callback.message.answer(f"Данные опроса сохранены!")
        await callback.message.answer(f"Опрос '{data['name']}' успешно создан.")

    except Exception as e:
        # Если произошла ошибка, информируем пользователя
        await callback.message.answer(
            "Произошла ошибка при сохранении опроса. Попробуйте снова."
        )
        print(f"Ошибка при сохранении опроса: {e}")

    await state.clear()
