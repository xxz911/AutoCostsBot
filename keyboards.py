from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('/start')],  # ВРЕМЕННАЯ КНОПКА
    [KeyboardButton('📊Статистика'), KeyboardButton('🌡️Установить лимит')],
    [KeyboardButton('🆘Помощь')]
])

kb_statistic = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('📊 за день'), KeyboardButton('📊 за месяц')],
    [KeyboardButton('📊 год'), KeyboardButton('📊 всего')],
    [KeyboardButton('Главное меню')]
])

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton('Главное меню'))
