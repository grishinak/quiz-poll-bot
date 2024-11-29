from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
import database.requests as rq

router = Router()

# FSM для подключения к лобби
class LobbyState(StatesGroup):
    waiting_for_lobby_id = State()


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
    await message.answer(f"Вы успешно подключились к лобби #{lobby_id}!")
    await state.clear()
