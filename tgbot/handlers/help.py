from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
help_text = """🤖 Список команд:\n\
\n/start - Перезапустить бота.\
\n/help - Справка о командах.\
\n/questions - Вопросы.\
\n/polls - Опросы.  \
\n/answers - Список ответов в ваших опросах. \
"""

# /help handler
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Answer help message with info from `help_text`"""
    await message.answer(help_text)
