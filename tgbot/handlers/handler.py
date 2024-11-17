from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import keyboards.start as kb
import database.requests as rq

router = Router()

start_text = (
    """С помощью этого бота Вы можете создать опрос с правильным ответом..\n ..."""
)
help_text = "Список команд:\n/start - инициализация бота.\n/help - получение информации о боте.\n ..."


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Answer start message with greeting from `start_text`"""
    await rq.set_user(
        message.from_user.id, message.from_user.first_name, message.from_user.last_name
    )
    await message.answer(start_text, reply_markup=kb.start_menu)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Answer help message with info from `help_text`"""
    await message.answer(help_text)


# #for repl
# @router.message(F.data =="reply")
# async def cmd_reply(message: Message):
#     await message.message.answer("you chose reply mes")

# #for inl
# @router.callback_query(F.data =="reply")
# async def cmd_reply(callback: CallbackQuery):
#     await callback.answer("you chose to touch button reply")
#     await callback.message.answer("you chose reply inl")
