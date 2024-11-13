from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Расписание на сегодня", callback_data="today_schedule")
    builder.button(text="Расписание на неделю", callback_data="week_schedule")
    builder.button(text="Редактировать расписание", callback_data="edit_schedule")
    return builder.as_markup()

def group_keyboard(groups):
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.button(text=group.name, callback_data=f"group:{group.id}")
    return builder.as_markup()

def weekday_keyboard():
    builder = InlineKeyboardBuilder()
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    for day in days:
        builder.button(text=day, callback_data=f"day:{day}")
    return builder.as_markup()