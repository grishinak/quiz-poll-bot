from aiogram.types import BotCommand
from aiogram import Bot

bot_commands = [
    BotCommand(command="start", description="🔄 Перезапустить бота"),
    BotCommand(command="help", description="📒 Справка о командах"),
    BotCommand(command="questions", description="❓Вопросы"),
    BotCommand(command="polls", description="📝 Опросы"),
    BotCommand(command="answers", description="📩 Список ответов в ваших опросах"),
    BotCommand(command="drop", description="🗑️ Сбросить сохраненные данные"),
]


async def set_commands(bot_: Bot):
    """
    Setting the commands to be displayed in the menu
    :param bot_: telegram bot
    """
    await bot_.set_my_commands(commands=bot_commands)
