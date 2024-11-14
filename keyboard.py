from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import Group, SessionLocal, Schedule


def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Расписание на сегодня", callback_data="today_schedule"),
         InlineKeyboardButton(text="Расписание на неделю", callback_data="week_schedule")],
        [InlineKeyboardButton(text="Редактировать расписание", callback_data="edit_schedule")]
    ])

def group_keyboard(groups, for_today=True):
    prefix = "today_group" if for_today else "week_group"
    buttons = [InlineKeyboardButton(text=group.name, callback_data=f"{prefix}:{group.id}") for group in groups]

    # Разделяем кнопки на строки по две в каждой
    inline_keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def weekday_keyboard(group_id):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    buttons = [
        InlineKeyboardButton(text=day.capitalize(), callback_data=f"day:{group_id}:{day}")
        for day in days
    ]

    # Разделяем кнопки на строки по две в каждой
    inline_keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# Клавиатура для редактирования расписания
def edit_schedule_keyboard(group_id, day):
    session = SessionLocal()
    schedule = session.query(Schedule).filter(Schedule.group_id == group_id, Schedule.day == day).all()
    buttons = [
        InlineKeyboardButton(text=f"Редактировать {item.time}", callback_data=f"edit:{item.id}")
        for item in schedule
    ]

    # Разделяем кнопки по две в ряд
    inline_keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)