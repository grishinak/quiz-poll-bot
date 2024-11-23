from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
help_text = """Список команд:\
\n/start - инициализация бота.\
\n/help - получение информации о боте.\
\n/create_poll - создание опроса.\
\n/poll_list - список созданных опросов.\
    \
\n/create_lobby - ...\
\n/lobbies_list - ...\
\n/connect_lobby - ...\
\n/start_poll - ...\
\n/end_poll - ...
"""

# /help handler
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Answer help message with info from `help_text`"""
    await message.answer(help_text)
