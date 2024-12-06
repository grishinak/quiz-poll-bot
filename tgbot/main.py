# importing for .env
import os
from dotenv import load_dotenv

# aiogram imports
import asyncio
from aiogram import Bot, Dispatcher


# importing all routers
from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.questions import router as questions_router
from handlers.polls import router as polls_router
from handlers.answers import router as show_answers_router
from handlers.drop import router as drop_router
from handlers.commands import set_commands

# db
from database.models import async_main


async def main():
    await async_main()  # create db
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    await set_commands(bot)
    for router in [
        start_router,
        help_router,
        questions_router,
        polls_router,
        show_answers_router,
        drop_router,
    ]:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        print(f"Error run bot: {Exception}")
