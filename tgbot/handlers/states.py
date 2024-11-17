from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

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
async def process_name(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(CreatePoll.answer)
    await message.answer("Введите ответ на свой вопрос (для подсчетов результатов):")


@router.message(CreatePoll.answer)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()  # get all data about poll from user
    await message.answer(
        f"Название опроса: {data['name']}\nВопрос: {data['question']}\nОтвет: {data['answer']}"
    )
    await state.clear()
