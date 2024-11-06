"""Обработчики для работы с расписанием"""
import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from datetime import datetime

# from app.schedule import schedule, full_schedule
from app.handlers.handlers_main import ScheduleStates

import app.keyboard as kb # Импорт кнопок
import json

# # Загрузка расписания из файла
# with open('schedule.json', 'r', encoding='utf-8') as f:
#     schedule_data = json.load(f)
# Функция для загрузки расписания из файла
def load_schedule_from_file(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        schedule = json.load(file)  # Загружаем данные из JSON-файла
    return schedule

# Пример использования
schedule_file_path = 'schedule.json'
schedule = load_schedule_from_file(schedule_file_path)

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

# # Обработчик для кнопок с полным расписанием
# @router.callback_query(F.data.in_({"christian_theology", "islamic_theology"}))
# async def send_full_schedule(call: CallbackQuery, state: FSMContext):
#     group = call.data  # Получаем группу из callback_data
#     schedule_text = full_schedule.get(group, 'Расписание не найдено.')
#
#     # keyboard = kb.keyboard_back
#     await state.set_state(ScheduleStates.BACK_WEEK_SCHEDULE)
#     # Отправляем сообщение с расписанием
#     await call.message.answer(f"Полное расписание для группы:\n{schedule_text}", reply_markup=kb.keyboard_back)
#     await call.answer()
#     # Имитация эффекта исчезновения с редактированием сообщения
#     await call.message.edit_text("Открываю расписание на неделю...")  # Заменяем сообщение на "..."
#     await asyncio.sleep(1)  # Делаем паузу в 1 секунду
#
#     # Удаляем предыдущее сообщение (сообщение с кнопками)
#     await call.message.delete()
#
# def get_current_class(group: str):
#     now = datetime.now()
#     weekday = now.strftime('%A').lower()
#     if group in schedule and weekday in schedule[group]:
#         return f"Текущие занятия: \n{schedule[group][weekday]}"
#     else:
#         return "Сегодня нет занятий."

# Обработчик для кнопок выбора группы
@router.callback_query(lambda call: call.data in ["islamic_theology", "christian_theology"])
async def send_schedule(call: CallbackQuery, state: FSMContext):
    await state.set_state(ScheduleStates.BACK_WEEK_SCHEDULE)
    group = call.data  # Получаем выбранную группу
    schedule_message = get_week_schedule(schedule, group)  # Формируем расписание

    # Разбиваем сообщение, если оно слишком длинное
    split_messages = split_long_message(schedule_message)

    for part in split_messages:
        await call.message.answer(part, parse_mode='HTML')  # Используем bot.send_message

# Функция для формирования расписания на неделю для выбранной группы
def get_week_schedule(schedule: dict, group: str) -> str:
    group_schedule = schedule[group]
    if group == 'islamic_theology':
        message = f"🗓Расписание на неделю для группы <b>Исламская теология</b>:\n\n"  # Заголовок
    else:
        message = f"🗓Расписание на неделю для группы <b>Христианская теология</b>:\n\n"  # Заголовок

    for day, subjects in group_schedule.items():
        message += (f"______________________________"
                    f"\n⭐️День недели - <b>{day}</b>:\n\n")  # Название дня

        if not subjects:  # Проверяем, есть ли занятия
            message += "  Нет занятий\n"
            continue

        for subject in subjects:
            subject_type = subject['Тип']
            time = subject['Время']
            course = subject['Предмет']
            teacher = subject['Преподаватель']
            building = subject['Корпус']
            floor = subject['Этаж']
            room = subject['Аудитория']

            # Формируем сообщение с расписанием с отступами
            message += (
                f"     {time}"
                f"     <b>{course}</b>"
                f"     {teacher} - ({building}, {floor}, {room})\n"
            )
            # # Формируем сообщение с расписанием с отступами
            # message += (
            #     f"  ➤ *{subject_type}*\n"
            #     f"     🕒 *Время:* {time}\n"
            #     f"     📚 *Предмет:* {course}\n"
            #     f"     👨‍🏫 *Преподаватель:* {teacher}\n"
            #     f"     🏢 *Корпус:* {building}, *Этаж:* {floor}, *Аудитория:* {room}\n\n"
            # )

    return message

# Функция для разбиения длинного сообщения на несколько частей
def split_long_message(message: str, max_length: int = 4096) -> list:
    # Если сообщение меньше лимита, возвращаем его как есть
    if len(message) <= max_length:
        return [message]

    # Разбиваем сообщение на части
    parts = []
    while len(message) > max_length:
        # Находим ближайший конец строки перед лимитом
        split_at = message[:max_length].rfind('\n')
        if split_at == -1:
            split_at = max_length
        parts.append(message[:split_at])
        message = message[split_at:]

    parts.append(message)
    return parts

# # Обработчик для кнопок с текущим занятием
# @router.callback_query(F.data.in_({"now_christian_theology", "now_islamic_theology"}))
# async def send_current_class_handler(callback: CallbackQuery, state: FSMContext):
#     group = callback.data.split("_")[1]  # Получаем название группы из callback_data
#     group = 'christian_theology' if group == 'christian' else 'islamic_theology'  # Преобразуем в название группы
#
#     current_class = get_current_class(group)
#
#     await state.set_state(ScheduleStates.BACK_TODAY_SCHEDULE)
#     await callback.message.answer(current_class, reply_markup=kb.keyboard_back)
#     # await callback.message.answer(current_class)
#     await callback.answer()
#     # Имитация эффекта исчезновения с редактированием сообщения
#     await callback.message.edit_text("Открываю расписание на сегодня...")  # Заменяем сообщение на "..."
#     await asyncio.sleep(1)  # Делаем паузу в 1 секунду
#
#     # Удаляем предыдущее сообщение (сообщение с кнопками)
#     await callback.message.delete()


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

