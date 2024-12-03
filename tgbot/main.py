# importing for .env
import os
from dotenv import load_dotenv

# aiogram imports
import asyncio
from aiogram import Bot, Dispatcher

# importing all routers
from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.create_question import router as create_poll_router
from handlers.questions_list import router as poll_list_router
from handlers.create_poll import router as create_lobby_router
from handlers.polls_list import router as lobbies_list_router
from handlers.connect_poll import router as connect_lobby_router
from handlers.show_answers import router as show_answers_router

# db
from database.models import async_main


async def main():
    await async_main()  # create db
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    for router in [
        start_router,
        help_router,
        create_poll_router,
        poll_list_router,
        create_lobby_router,
        lobbies_list_router,
        connect_lobby_router,
        show_answers_router,
    ]:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        print(f"Error run bot: {Exception}")
