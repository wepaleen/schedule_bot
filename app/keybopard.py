from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

inline_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Христианская теология 13.1-202А', callback_data='christian_theology')],
    [InlineKeyboardButton(text='Исламская теология 13.1-202Б', callback_data='islamic_theology')]
])



# Создаем кнопки для выбора группы
buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Христианская теология", callback_data="now_christian_theology")],
    [InlineKeyboardButton(text="Исламская теология", callback_data="now_islamic_theology")]
])
# keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])



