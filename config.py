import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("text.env"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS").split(",")]

# имя пользователя БД
username = "admin"
# Пароль к БД
password = "234de32fgdf"
# Адрес хоста с БД
localhost = "45.151.30.108"
# Имя БД
dbname = "schedule_db"
