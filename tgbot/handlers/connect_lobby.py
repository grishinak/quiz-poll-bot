from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
import database.requests as rq

import keyboards.connect_lobby as kb

router = Router()

# FSM для подключения к лобби
class LobbyState(StatesGroup):
    waiting_for_lobby_id = State()
    answer = State()


# обработка нажатия кнопки from /start и переход в состояние
@router.callback_query(F.data == "connect_lobby")
async def clb_connect_lobby(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы подключаетесь к лобби.")
    await callback.message.answer("К какому лобби вы хотите подключиться?")
    await state.set_state(LobbyState.waiting_for_lobby_id)


@router.message(Command("connect_lobby"))
async def cmd_connect_lobby(message: Message, state: FSMContext):
    await message.answer("К какому лобби вы хотите подключиться?")
    await state.set_state(LobbyState.waiting_for_lobby_id)


@router.message(LobbyState.waiting_for_lobby_id)
async def process_lobby_id(message: Message, state: FSMContext):
    try:
        lobby_id = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите действительный ID лобби.")
        return

    if not await rq.check_lobby_exists(lobby_id):
        await message.answer("Лобби не существует.")
        return

    if await rq.check_if_participant_exists(lobby_id, message.from_user.id):
        await message.answer("Вы уже подключены к этому лобби!")
        return

    await rq.set_lobby_participant(lobby_id, message.from_user.id)
    await state.update_data(lobby_id=message.text)
    await message.answer(f"Вы успешно подключились к лобби #{lobby_id}!")

    # TODO: go to state to give answer if creater sterted.

    # await state.clear()

    # Обработка нажатия кнопки (from start) и переход в состояние


@router.callback_query(F.data == "give_answer")
async def give_answer_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали отвечать на вопрос")  # alert

    await state.set_state(LobbyState.answer)  # goes to state
    await callback.message.answer("Введите ваш ответ: ")  # message in chat


@router.message(LobbyState.answer)
async def process_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()  # get all data about poll from user
    await message.answer(
        f"Все ли верно?\n\nОтвет: {data['answer']}",
        reply_markup=kb.check_menu,  # buttons for check
    )


# Обработка нажатия кнопки (from answer) и переход в состояние
@router.callback_query(F.data == "check_answer_false")
async def process_check_false(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Данные не верны.")
    await callback.answer("Сначала")  # alert
    await callback.message.answer("Вы начали ввод ответа сначала!")  # message in chat

    await state.set_state(LobbyState.answer)  # goes to state
    await callback.message.answer("Введите ваш ответ: ")


# Обработка нажатия кнопки (from answer) и переход в состояние
@router.callback_query(F.data == "check_answer_true")
async def process_check_true(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Успешно")  # alert
    await callback.message.edit_text("Данные верны.", reply_markup=None)
    data = await state.get_data()

    participant_id = callback.from_user.id
    try:
        if await rq.is_lobby_collecting(data["lobby_id"]):
            answer_id = await rq.set_answer(
                lobby_id=data["lobby_id"],
                participant_id=participant_id,
                user_answer=data["answer"],
            )

            # Отправляем сообщение пользователю о том, что опрос сохранен
            await callback.message.answer(f"Ваш ответ '{data['answer']}' сохранен!")
        else:
            await callback.message.answer(
                f"Время для ответа вышло. Опрос уже завершен."
            )

    except Exception as e:
        # Если произошла ошибка, информируем пользователя
        await callback.message.answer(
            "Произошла ошибка при сохранении ответа. Попробуйте снова."
        )
        print(f"Ошибка при сохранении ответа: {e}")

    await state.clear()
