from aiogram.fsm.state import StatesGroup, State


class CreatePoll(StatesGroup):
    name = State()
    question = State()
    answer = State()
