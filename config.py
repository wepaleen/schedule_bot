import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from datetime import datetime as dt

load_dotenv('/app/utils/config/.env')
# load_dotenv(find_dotenv("schedule.env"))

# Список ID администраторов
admin_ids = [820372096]  # Замените на реальные ID администраторов
# Подключение к БД

async def get_time() -> str:
    """Возвращает сегодняшнюю дату в строковом виде в формате  ДД.ММ.ГГГГ"""
    return dt.now().strftime("%d.%m.%Y")

@dataclass
class DBConfig:
    db_login = os.environ.get("LOGIN")
    db_pass = os.environ.get("PASS")
    db_host = os.environ.get("HOST")
    db_name = os.environ.get("DBNAME")

    url = f"postgresql+asyncpg://{db_login}:{db_pass}@{db_host}:5432/{db_name}"