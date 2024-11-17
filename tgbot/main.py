# importing for .env
import os
from dotenv import load_dotenv

# aiogram imports
import asyncio
from aiogram import Bot, Dispatcher

# importing all routers
from handlers.handler import router as handler_router
from handlers.fsm import router as fsm_router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    for router in [
        handler_router,
        fsm_router,
    ]:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        print(f"Error run bot: {Exception}")
