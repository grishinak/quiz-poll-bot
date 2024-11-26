from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database.requests as rq

router = Router()

# class with fsm states
class ConnectLobby(StatesGroup):
    lobby = State()


# Обработка команды и переход в состояние
@router.message(Command("connect_lobby"))
async def process_connect_lobby_cmd(message: Message, state: FSMContext):
    await message.answer("Вы подсоединяетесь к лобби!")  # message in chat

    await state.set_state(ConnectLobby.lobby)  # goes to state
    await message.answer(
        "Введите номер лобби (после#), который вам должен сообщить автор опроса для прохождения:"
    )


@router.message(ConnectLobby.lobby)
async def process_lobby(message: Message, state: FSMContext):
    await state.update_data(lobby=message.text)
    data = await state.get_data()

    try:
        # Проверяем, существует ли лобби
        lobby_exists = await rq.check_lobby_exists(data["lobby"])
        if not lobby_exists:
            await message.answer(
                "Лобби с таким ID не существует. Пожалуйста, проверьте номер."
            )
            return

        # Проверяем, не является ли пользователь уже участником лобби
        already_in_lobby = await rq.check_if_participant_exists(
            data["lobby"], message.from_user.id
        )
        if already_in_lobby:
            await message.answer("Вы уже подключены к этому лобби.")
            return

        # Если все проверки пройдены, добавляем пользователя в лобби
        lobby_participant = await rq.set_lobby_participant(
            lobby_id=data["lobby"], user_id=message.from_user.id
        )

        await message.answer(
            f"Теперь вы участник лобби! Ожидайте, пока организатор не запустит опрос."
        )

    except Exception as e:
        await message.answer(
            "Произошла ошибка при подключении к лобби. Попробуйте снова."
        )
        print(f"Ошибка при подключении к лобби: {e}")

    await state.clear()
