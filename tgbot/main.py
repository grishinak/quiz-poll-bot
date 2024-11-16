import os
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher

from handlers.handler import router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        print(f"Error run bot: {Exception}")
