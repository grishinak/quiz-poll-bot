from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import keyboards.start as kb
import database.requests as rq

router = Router()
start_text = """С помощью этого бота Вы можете проводить опросы.\n"""

# /start handler
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Answer start message with greeting from `start_text`"""
    await rq.set_user(
        message.from_user.id, message.from_user.first_name, message.from_user.last_name
    )
    await message.answer(start_text, reply_markup=kb.start_menu)
