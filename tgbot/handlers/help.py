from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
help_text = """🤖 Список команд:\n\
\n/start - Перезапустить бота.\
\n/help - Справка о командах.\
\n/create_question - Создание вопроса.\
\n/questions_list - Список созданных опросов.\
\n/create_poll - Создать опрос с вопросом. \
\n/polls_list - Список опросов. \
\n/connect_poll - Подключиться к созданному опросу. \
\n/show_answers - Список ответов из опросов. \
"""

# /help handler
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Answer help message with info from `help_text`"""
    await message.answer(help_text)
