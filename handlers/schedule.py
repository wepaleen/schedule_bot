from datetime import datetime
import locale

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.orm import Session
from db import SessionLocal, Group, Schedule
from keyboard import main_menu_keyboard, group_keyboard, weekday_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать! Выберите опцию:", reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "today_schedule")
async def show_today_schedule(call: CallbackQuery):
    session = SessionLocal()
    groups = session.query(Group).all()
    await call.message.answer("Выберите группу:", reply_markup=group_keyboard(groups))

@router.callback_query(F.data == "week_schedule")
async def show_today_schedule(call: CallbackQuery):
    session = SessionLocal()
    groups = session.query(Group).all()
    await call.message.answer("Выберите группу:", reply_markup=group_keyboard(groups))

@router.callback_query(F.data.startswith("group:"))
async def select_group(call: CallbackQuery):
    group_id = int(call.data.split(":")[1])
    group_name = str(call.data.split(":")[1])
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    today = datetime.now().strftime("%A").capitalize()
    session = SessionLocal()
    schedule = session.query(Schedule).filter(Schedule.group_id == group_id, Schedule.day == today).all()

    if not schedule:
        await call.message.answer("Сегодня занятий нет.")
        return

    message = "\n".join([f"{item.time} - {item.subject} - {item.teacher} - {item.building} - {item.floor} - {item.room}" for item in schedule])
    await call.message.answer(f'''Расписание на сегодня для группы {group_name}:\n{message}''')

@router.callback_query(F.data.startswith("groups:"))
async def select_group(call: CallbackQuery):
    group_id = int(call.data.split(":")[1])
    today = datetime.now().strftime("%A")
    session = SessionLocal()
    schedule = session.query(Schedule).filter(Schedule.group_id == group_id, Schedule.day == today).all()

    if not schedule:
        await call.message.answer("Сегодня занятий нет.")
        return
    try:
        message = "\n".join([f"{item.time} - {item.subject}" for item in schedule])
        await call.message.answer(f"Расписание на сегодня:\n{message}")
    except Exception as e:
        print(e)