from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import keyboards.keyboard as kb

router = Router()


@router.message(Command("create_poll"))
async def cmd_help(message: Message):
    """Creating poll func"""
    await message.answer("Ceating poll")
