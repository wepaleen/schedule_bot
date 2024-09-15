import asyncio
import types

from aiogram import F, Router
from aiogram.client import bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction # Уведомление о том, что бот пишет ответ
from datetime import datetime
from app.schedule import schedule, full_schedule


import app.keybopard as kb # Импорт кнопок

router = Router() # Замена dp


# Команда /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer(f'Выберите группу, чтобы получить полное расписание:', reply_markup=kb.inline_main)

# Команда /now
@router.message(Command('now'))
async def send_current_class(message: Message):
    # Предположим, что для простоты пользователь выбирает только одну из двух групп.
    # В реальной ситуации вы можете добавить регистрацию пользователя и привязку к его группе.

    # Пример для христианской теологии (можно заменить на реальный выбор пользователя)
    # group = 'christian_theology' or 'islamic_theology' # или 'islamic_theology'
    #
    # current_class = get_current_class(group)
    #
    # await message.answer(current_class)
    await message.answer("Выберите группу для вывода текущего занятия:", reply_markup=kb.buttons)

# Команда /help
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('<b>Правила эксплуатации бота расписания для студентов КФУ:</b>'
                         '\n▪️Для просмотра полного расписания введите команду: /start'
                         '\n▪️Чтобы увидеть занятия, которые идут прямо сейчас введите команду: /now'
                         '\n\n<b>Контакты:</b>'
                         'Разработчик - Руслан Мамахаев(<i>@wwdcdev</i>)', parse_mode='html')


# Обработчик для кнопок с полным расписанием
@router.callback_query(F.data.in_({"christian_theology", "islamic_theology"}))
async def send_full_schedule(call: CallbackQuery):
    group = call.data  # Получаем группу из callback_data
    schedule_text = full_schedule.get(group, 'Расписание не найдено.')

    # Отправляем сообщение с расписанием
    await call.message.answer(f"Полное расписание для группы:\n{schedule_text}")
    await call.answer()
    # Имитация эффекта исчезновения с редактированием сообщения
    await call.message.edit_text("...")  # Заменяем сообщение на "..."
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
async def send_current_class_handler(callback: CallbackQuery):
    group = callback.data.split("_")[1]  # Получаем название группы из callback_data
    group = 'christian_theology' if group == 'christian' else 'islamic_theology'  # Преобразуем в название группы

    current_class = get_current_class(group)

    await callback.message.answer(current_class)
    await callback.answer()
    # Имитация эффекта исчезновения с редактированием сообщения
    await callback.message.edit_text("...")  # Заменяем сообщение на "..."
    await asyncio.sleep(5)  # Делаем паузу в 1 секунду

    # Удаляем предыдущее сообщение (сообщение с кнопками)
    await callback.message.delete()
