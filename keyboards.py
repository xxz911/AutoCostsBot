"""Клавиатуры"""


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура главного меню
kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('/start')],  # ВРЕМЕННАЯ КНОПКА
    [KeyboardButton('📊Статистика'), KeyboardButton('🌡️Установить лимит')],
    [KeyboardButton('🆘Помощь')]
])

# Клавиатура выбора периода статистики
kb_statistic = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('📊 дневная'), KeyboardButton('📊 месячная')],
    [KeyboardButton('📊 годовая'), KeyboardButton('📊 общая')],
    [KeyboardButton('Главное меню')]
])

# Клавиатура для перехода в главное меню
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton('Главное меню'))
