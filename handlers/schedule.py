from datetime import datetime
import locale

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.orm import Session
from db import SessionLocal, Group, Schedule
from keyboard import main_menu_keyboard, group_keyboard, weekday_keyboard

router = Router()

# Установка локали (для расписания на сегодня и неделю)
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


# Команда для старта
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать! Выберите опцию:", reply_markup=main_menu_keyboard())


# Обработка кнопки "Расписание на сегодня"
@router.callback_query(F.data == "today_schedule")
async def show_today_schedule(call: CallbackQuery):
    session = SessionLocal()
    groups = session.query(Group).all()
    await call.message.answer("Выберите группу для расписания на сегодня:", reply_markup=group_keyboard(groups))


# Обработка кнопки "Расписание на неделю"
@router.callback_query(F.data == "week_schedule")
async def show_week_schedule(call: CallbackQuery):
    session = SessionLocal()
    groups = session.query(Group).all()
    await call.message.answer("Выберите группу для расписания на неделю:", reply_markup=group_keyboard(groups, for_today=False))


# Обработка выбора группы для расписания на сегодня
@router.callback_query(F.data.startswith("today_group:"))
async def select_group_today(call: CallbackQuery):
    group_id = int(call.data.split(":")[1])
    today = datetime.now().strftime("%A").capitalize()
    session = SessionLocal()
    schedule = session.query(Schedule).filter(Schedule.group_id == group_id, Schedule.day == today).all()

    if not schedule:
        await call.message.answer("Сегодня занятий нет.")
        return

    msg = ("1-Время 2-Предмет 3-Преподаватель 3-Учебное здание 4-Этаж 5-Аудитория")
    message = "\n".join([
        f"{item.time} - {item.subject} - {item.teacher} - {item.building} - {item.floor} - {item.room}"
        for item in schedule
    ])
    await call.message.answer(f'Расписание на сегодня ({today}):\n{msg} \n\n{message}')


# Обработка выбора группы для расписания на неделю
@router.callback_query(F.data.startswith("week_group:"))
async def select_group_week(call: CallbackQuery):
    group_id = int(call.data.split(":")[1])
    await call.message.answer("Выберите день недели:", reply_markup=weekday_keyboard(group_id))


# Обработка выбора дня недели для расписания на неделю
@router.callback_query(F.data.startswith("day:"))
async def select_day(call: CallbackQuery):
    data = call.data.split(":")
    group_id = int(data[1])
    day = data[2]

    # Убедитесь, что день недели пишется с заглавной буквы и на русском
    day = day.capitalize()

    session = SessionLocal()
    schedule = session.query(Schedule).filter(Schedule.group_id == group_id, Schedule.day == day).all()

    if not schedule:
        await call.message.answer(f"На {day} занятий нет.")
        return

    message = "\n".join([
        f"{item.time} - {item.subject} - {item.teacher} - {item.building} - {item.floor} - {item.room}"
        for item in schedule
    ])
    await call.message.answer(f'Расписание на {day}:\n{message}')
