"""Контроллер"""

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from settings import API_TOKEN
from messages import PROBLEM_MESSAGE, HELP_MESSAGE, NOT_TEXT_MESSAGE, BAD_TEXT_MESSAGE
from keyboards import kb, kb_statistic
from utils import Filter, STATISTIC_TIME
from sqlite import db_create
from utils_db import db_is_ready, get_limit, set_limit, set_cost, get_statistic, del_cost

# Включаем логирование
file_log = logging.FileHandler("log.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    level=logging.ERROR,
                    format="%(asctime)s %(levelname)s |  %(lineno)d %(funcName)s: %(message)s"
                    )

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Выполнение при запуске
async def on_startup(_):
    await db_create()
    print('___Бот запустился!___')


# Обработка команды 'Старт'
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    try:
        await db_is_ready(message)
        await cmd_help_kb(message=message)
        await cmd_main_kb(message=message)
    except Exception:
        await message.answer(
            text=PROBLEM_MESSAGE,
            reply_markup=kb
        )


# Обработка кнопки 'Главное меню'
@dp.message_handler(Text(equals='🏠Главное меню'))
async def cmd_main_kb(message: types.Message) -> None:
    await message.answer(text="📝Напишите мне свои расходы", reply_markup=kb)
    await message.delete()


# Обработка кнопки 'Статистика'
@dp.message_handler(Text(equals='📜Статистика'))
async def cmd_statistic_kb(message: types.Message) -> None:
    await message.answer(text="☑️Выбери нужную статистику", reply_markup=kb_statistic)
    await message.delete()


# Обработка кнопки 'Помощь'
@dp.message_handler(Text(equals='🆘Помощь'))
async def cmd_help_kb(message: types.Message) -> None:
    await message.answer(
        text=HELP_MESSAGE,
        parse_mode="HTML",
        reply_markup=kb
    )


# Обработка кнопки 'Установить лимит'
@dp.message_handler(Text(equals='🌡️Установить лимит'))
async def cmd_limit_kb(message: types.Message) -> None:
    await get_limit(message)
    await message.delete()


# Обработка сообщений для установки лимита на расходы
@dp.message_handler(lambda message: Filter.is_handler_limit(message.text))
async def cmd_set_limit(message: types.Message) -> None:
    await set_limit(message)


# Обработка сообщений для сохранения расходов
@dp.message_handler(lambda message: Filter.is_handler_cost(message.text))
async def cmd_set_cost(message: types.Message) -> None:
    await set_cost(message)


# Обработка сообщений для удаления расходов
@dp.message_handler(lambda message: message.text.startswith('/del'))
async def cmd_del_cost(message: types.Message) -> None:
    await del_cost(message)


# Обработка сообщений для отправки статистики
@dp.message_handler(lambda message: message.text in STATISTIC_TIME)
async def cmd_send_statistic(message: types.Message) -> None:
    await get_statistic(message)
    await message.delete()


# Обработка невалидных сообщений
@dp.message_handler(content_types=types.ContentType.ANY)
async def cmd_exceptions(message: types.Message) -> None:
    text = BAD_TEXT_MESSAGE if message.text else NOT_TEXT_MESSAGE
    await message.reply(text=text, reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
