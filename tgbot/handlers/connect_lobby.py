from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database.requests as rq

# import keyboards.connect_lobby as kb

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
        "Введите номер лобби (после#) который вам должен сообщить автор опроса для прохождения:"
    )


@router.message(ConnectLobby.lobby)
async def process_lobby(message: Message, state: FSMContext):
    await state.update_data(lobby=message.text)
    # TODO: checks if the lobby exists
    data = await state.get_data()
    try:
        # Сохраняем участника лобби в базе данных
        # #TODO: проверять, есть ли в лобби уже участник или нет. избегать повторного подключения 1 и того же.
        lobby_participant_id = await rq.set_lobby_participant(
            lobby_id=data["lobby"], user_id=message.from_user.id
        )

        # Отправляем сообщение пользователю о том, что лобби сохранено
        await message.answer(
            f"Теперь вы участник лобби! Ожидайте, пока организатор не запустит опрос."
        )

    # TODO: выход из лобби
    # TODO: обработка ввода ответов на опрос тут?? or in poll.py?

    except Exception as e:
        # Если произошла ошибка, информируем пользователя
        await message.answer(
            "Произошла ошибка при подключении к лобби. Попробуйте снова."
        )
        print(f"Ошибка при подключении к лобби: {e}")

    await state.clear()
