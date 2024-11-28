from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Bot
from aiogram.fsm.state import State, StatesGroup  # Импортируем StatesGroup

import database.requests as rq

# Определяем состояние для FSM с использованием StatesGroup
class LobbyState(StatesGroup):  # Наследуем от StatesGroup
    waiting_for_lobby_id = State()  # Ожидаем ID лобби


router = Router()

# Обработчик команды /connect_lobby
@router.message(Command("connect_lobby"))
async def cmd_connect_lobby(message: Message, state: FSMContext):
    # Запрашиваем ID лобби
    await message.answer("К какому лобби вы хотите подключиться?")
    await state.set_state(
        LobbyState.waiting_for_lobby_id
    )  # Переход к состоянию ожидания ID лобби


# Обработчик для получения ID лобби и подключения пользователя
@router.message(LobbyState.waiting_for_lobby_id)
async def process_lobby_id(message: Message, state: FSMContext, bot: Bot):
    try:
        # Преобразуем введенный текст в ID лобби
        lobby_id = int(message.text)
    except ValueError:
        # Если ID не является числом
        await message.answer("Пожалуйста, введите действительный ID лобби.")
        return

    # Проверим существование лобби
    if not await rq.check_lobby_exists(lobby_id):
        await message.answer("Лобби не существует.")
        return

    # Добавляем пользователя в лобби
    if await rq.check_if_participant_exists(lobby_id, message.from_user.id):
        await message.answer("Вы уже в этом лобби!")
        return

    # Подключаем пользователя к лобби
    await rq.set_lobby_participant(lobby_id, message.from_user.id)
    await message.answer(f"Вы подключились к лобби {lobby_id}!")

    # Получаем poll_id и сам вопрос
    poll_id = await rq.get_poll_id_for_lobby(lobby_id)
    question = await rq.get_poll_question(poll_id)

    # Получаем всех участников лобби
    participants = await rq.get_lobby_participants(lobby_id)

    # Отправим вопрос всем участникам
    for participant_id in participants:
        # отправим вопрос каждому участнику лобби
        await bot.send_message(
            participant_id, f"Вопрос: {question}"
        )  # сейчас сразу при подключении отправляется всем

    # Завершаем сессию
    await state.clear()  # Завершаем FSM после успешного подключения
