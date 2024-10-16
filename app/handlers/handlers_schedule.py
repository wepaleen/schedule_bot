"""Обработчики для работы с расписанием"""
import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from datetime import datetime

from app.schedule import schedule, full_schedule
from app.handlers.handlers_main import ScheduleStates

import app.keyboard as kb # Импорт кнопок

router = Router() # Замена dp

# Хендлер для кнопки "Расписание на неделю"
@router.callback_query(F.data == "inline_week_schedule")
async def inline_week_schedule(call: CallbackQuery,  state: FSMContext):
    # keyboard = kb.keyboard_week_schedule
    await state.set_state(ScheduleStates.BACK_WEEK_SCHEDULE)
    await call.message.delete()
    await call.message.answer('Вы выбрали расписание на неделю:', reply_markup=kb.keyboard_week_schedule)

# Хендлер для кнопки "Расписание на сегодня"
@router.callback_query(F.data == "inline_today_schedule")
async def inline_today_schedule(call: CallbackQuery, state: FSMContext):
    await state.set_state(ScheduleStates.TODAY_SCHEDULE)
    await call.message.delete()
    await call.message.answer('Вы выбрали расписание на сегодня:', reply_markup=kb.keyboard_today_schedule)

# Обработчик для кнопок с полным расписанием
@router.callback_query(F.data.in_({"christian_theology", "islamic_theology"}))
async def send_full_schedule(call: CallbackQuery, state: FSMContext):
    group = call.data  # Получаем группу из callback_data
    schedule_text = full_schedule.get(group, 'Расписание не найдено.')

    # keyboard = kb.keyboard_back
    await state.set_state(ScheduleStates.BACK_WEEK_SCHEDULE)
    # Отправляем сообщение с расписанием
    await call.message.answer(f"Полное расписание для группы:\n{schedule_text}", reply_markup=kb.keyboard_back)
    await call.answer()
    # Имитация эффекта исчезновения с редактированием сообщения
    await call.message.edit_text("Открываю расписание на неделю...")  # Заменяем сообщение на "..."
    await asyncio.sleep(1)  # Делаем паузу в 1 секунду

    # Удаляем предыдущее сообщение (сообщение с кнопками)
    await call.message.delete()

def get_current_class(group: str):
    now = datetime.now()
    weekday = now.strftime('%A').lower()
    if group in schedule and weekday in schedule[group]:
        return f"Текущие занятия: \n{schedule[group][weekday]}"
    else:
        return "Сегодня нет занятий."


# Обработчик для кнопок с текущим занятием
@router.callback_query(F.data.in_({"now_christian_theology", "now_islamic_theology"}))
async def send_current_class_handler(callback: CallbackQuery, state: FSMContext):
    group = callback.data.split("_")[1]  # Получаем название группы из callback_data
    group = 'christian_theology' if group == 'christian' else 'islamic_theology'  # Преобразуем в название группы

    current_class = get_current_class(group)

    await state.set_state(ScheduleStates.BACK_TODAY_SCHEDULE)
    await callback.message.answer(current_class, reply_markup=kb.keyboard_back)
    # await callback.message.answer(current_class)
    await callback.answer()
    # Имитация эффекта исчезновения с редактированием сообщения
    await callback.message.edit_text("Открываю расписание на сегодня...")  # Заменяем сообщение на "..."
    await asyncio.sleep(1)  # Делаем паузу в 1 секунду

    # Удаляем предыдущее сообщение (сообщение с кнопками)
    await callback.message.delete()


# Обработка нажатия на кнопку "Назад"
@router.callback_query(F.data == "btn_back")
async def back_button(call: CallbackQuery, state: FSMContext):
    # Получаем текущее состояние пользователя
    current_state = await state.get_state()

    # Возвращаемся на шаг назад в зависимости от текущего состояния
    if current_state == ScheduleStates.WEEK_SCHEDULE:
        # Если пользователь был на расписании на неделю, возвращаем в главное меню
        await state.set_state(ScheduleStates.MAIN_MENU)
        await call.message.delete()
        await call.message.answer("Выберите опцию:", reply_markup=kb.inline_main)

    elif current_state == ScheduleStates.TODAY_SCHEDULE:
        # Если пользователь был на расписании на сегодня, возвращаем в главное меню
        await state.set_state(ScheduleStates.MAIN_MENU)
        await call.message.delete()
        await call.message.answer("Выберите опцию:", reply_markup=kb.inline_main)

    elif current_state == ScheduleStates.BACK_WEEK_SCHEDULE:
        await state.set_state(ScheduleStates.WEEK_SCHEDULE)
        await call.message.delete()
        await call.message.answer("Выберите опцию:", reply_markup=kb.keyboard_week_schedule)

    elif current_state == ScheduleStates.BACK_TODAY_SCHEDULE:
        await state.set_state(ScheduleStates.TODAY_SCHEDULE)
        await call.message.delete()
        await call.message.answer("Выберите опцию:", reply_markup=kb.keyboard_today_schedule)

