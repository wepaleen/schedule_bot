import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import schedule, admin

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    os.makedirs("./utils/log", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename="utils/log/bot_log.log",
        filemode="w",
        encoding="utf-8",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    dp.include_router(schedule.router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())