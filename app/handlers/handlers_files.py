"""Обработчики для работы с файлами"""
import os

import asyncpg
import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from db.database import add_user, save_file_to_db, get_user_id

router = Router()

# Функция для сохранения информации о файле в базе данных
async def save_file_to_db(user_id, file_name, file_path):
    conn = await asyncpg.connect(database='your_db', user='your_user', password='your_password')
    await conn.execute('''
        INSERT INTO files(user_id, file_name, file_path)
        VALUES($1, $2, $3)
    ''', user_id, file_name, file_path)
    await conn.close()

@router.message(Command('my_files'))
async def list_files(message: Message):
    # Запрашиваем файлы пользователя из базы данных
    user_id = message.from_user.id
    await message.delete()
    # await message.answer('Вы выбрали расписание на неделю:', reply_markup=kb.keyboard_week_schedule)
    conn = await asyncpg.connect(database='your_db', user='your_user', password='your_password')
    rows = await conn.fetch('SELECT file_name, file_path FROM files WHERE user_id = $1', user_id)
    await conn.close()

    if not rows:
        await message.answer("У вас нет сохраненных файлов.")
        return

    # Отправляем список файлов с кнопками для скачивания
    for row in rows:
        file_name = row['file_name']
        file_path = row['file_path']
        from aiohappyeyeballs import types
        await message.answer(file_name, reply_markup=types.InlineKeyboardMarkup().add(
            InlineKeyboardButton('Скачать', url=f"http://your_domain.com/{file_path}"),
            types.InlineKeyboardButton('Удалить', callback_data=f'delete_{file_name}')
        ))

# @router.message(F.document)
# async def handle_document(message: Message):
#     document = message.document  # Получаем объект документа из сообщения
#     file_name = document.file_name  # Имя файла
#     file_id = document.file_id  # Идентификатор файла (нужен для загрузки)
#
#     # Скачиваем файл через Telegram API
#     file_info = await message.bot.get_file(file_id)
#     file_content = await message.bot.download_file(file_info.file_path)
#
#     # Сохраняем файл на сервере
#     file_path = save_file(file_name, file_content)
#
#     # Сохраняем информацию о файле в базу данных (добавь свою функцию для работы с БД)
#     await save_file_to_db(message.from_user.id, file_name, file_path)
#
#     # Отправляем сообщение пользователю
#     await message.answer(f"Файл {file_name} успешно сохранен.")