from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards.create_poll as kb

router = Router()


class CreatePoll(StatesGroup):
    name = State()
    question = State()
    answer = State()


# Обработка нажатия кнопки (from start) и переход в состояние
@router.callback_query(F.data == "create_poll")
async def process_create_poll(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали создание опроса")  # alert
    await callback.message.answer("Вы начали создание опроса!")  # message in chat

    await state.set_state(CreatePoll.name)  # goes to state
    await callback.message.answer("Введите название опроса:")


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
        reply_markup=kb.check_menu,
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
    data = await state.get_data()  # TODO: need to save to db
    await callback.message.answer("Данные опроса сохранены!")
    await callback.message.answer(f"Опрос {data['name']} успешно создан!")

    await state.clear()
