from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('/start')],  # ВРЕМЕННАЯ КНОПКА
    [KeyboardButton('📊Статистика'), KeyboardButton('🌡️Установить лимит')],
    [KeyboardButton('🆘Помощь')]
])

kb_statistic = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('📊 дневная'), KeyboardButton('📊 месячная')],
    [KeyboardButton('📊 годовая'), KeyboardButton('📊 общая')],
    [KeyboardButton('Главное меню')]
])

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton('Главное меню'))
