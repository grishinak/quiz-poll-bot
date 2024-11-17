from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import keyboards.keyboard as kb

router = Router()

start_text = """Hello! I can help you with poll organisation.\n ..."""
help_text = (
    "List of commands:\n/start - initialising bot.\n/help - get info about bot.\n ..."
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Answer start message with greeting from `start_text`"""
    await message.answer(start_text, reply_markup=kb.menu)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Answer help message with info from `help_text`"""
    await message.answer(help_text)
