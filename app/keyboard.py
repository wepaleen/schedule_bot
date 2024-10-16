from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


#Создаем клавиатуру с выбором расписания на неделю
keyboard_week_schedule = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Христианская теология 13.1-202А', callback_data='christian_theology')],
        [InlineKeyboardButton(text='Исламская теология 13.1-202Б', callback_data='islamic_theology')],
        [InlineKeyboardButton(text='Назад', callback_data='btn_back')]])


# Создаем клавиатуру с выбором расписания на сегодня
keyboard_today_schedule = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Христианская теология", callback_data="now_christian_theology"),
        InlineKeyboardButton(text="Исламская теология", callback_data="now_islamic_theology")],
        [InlineKeyboardButton(text='Назад', callback_data='btn_back')]])


inline_main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Расписание на неделю', callback_data='inline_week_schedule'),
        InlineKeyboardButton(text='Расписание на сегодня', callback_data='inline_today_schedule')],
        [InlineKeyboardButton(text='Домашнее задание', callback_data='basket')]])


keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='btn_back')]])
