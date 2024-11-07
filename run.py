import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import schedule_router, main_router, files_router  # Импортируем все роутеры
from config import DBConfig
from db.connection import get_engine, session_maker


async def main():
    os.makedirs("./utils/log", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename="utils/log/bot_log.log",
        filemode="w",
        encoding="utf-8",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    bot = Bot(os.environ.get("BOT_TOKEN"))
    async_ = get_engine(DBConfig.url)
    # session = session_maker(async_.engine)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
    dp.include_router(schedule_router)
    dp.include_router(files_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except:
        print('Exit')