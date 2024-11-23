from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database.requests as rq

# import keyboards.create_lobby as kb

router = Router()

# class with fsm states
class CreateLobby(StatesGroup):
    poll = State()


# # Обработка нажатия кнопки ?from where?? и переход в состояние
# @router.callback_query(F.data == "create_lobby")
# async def process_create_lobby_clb(callback: CallbackQuery, state: FSMContext):
#     await callback.answer("Вы начали создание лобби")  # alert
#     await callback.message.answer("Вы начали создание лобби!")  # message in chat

#     await state.set_state(CreateLobby.poll)  # goes to state
#     await callback.message.answer("Введите номер опроса для прохождения:")


# Обработка команды и переход в состояние
@router.message(Command("create_lobby"))
async def process_create_lobby_cmd(message: Message, state: FSMContext):
    await message.answer("Вы начали создание лобби!")  # message in chat

    await state.set_state(CreateLobby.poll)  # goes to state
    await message.answer("Введите номер опроса (после#) для прохождения:")


@router.message(CreateLobby.poll)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(poll=message.text)
    # TODO: checks if the poll id is from author`s polls
    data = await state.get_data()
    try:
        # Сохраняем лобби в базе данных
        lobby_id = await rq.set_lobby(
            poll_id=data["poll"], creator_id=message.from_user.id
        )

        # Отправляем сообщение пользователю о том, что лобби сохранено
        await message.answer(
            f"Лобби создано! Можете сообщить участникам, чтобы они подключались к лобби #{lobby_id}."
        )

    except Exception as e:
        # Если произошла ошибка, информируем пользователя
        await message.answer("Произошла ошибка при создании лобби. Попробуйте снова.")
        print(f"Ошибка при создании лобби: {e}")

    await state.clear()


# TODO: delete lobbies
