"""Контроллер"""


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import API_TOKEN
from messages import *
from keyboards import *
from utils import *
from exceptions import *

# Включаем логирование
# logging.basicConfig(level=logging.DEBUG)

# Создаем хранилище состояний
storage = MemoryStorage()

# Инициализируем бота и dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Функция при запуске
async def on_startup(_):
    print('___Бот запустился!___')


# Вывод приветствия
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    f_name = message.from_user.first_name
    await message.answer(
        text=get_start_message(f_name),
        parse_mode="HTML",
        reply_markup=kb
    )
    await send_help(message=message)
    await send_main(message=message)


# Кнопка Главного меню
@dp.message_handler(Text(equals='Главное меню'))
async def send_main(message: types.Message) -> None:
    await message.answer(text="📝Напиши мне свои расходы", reply_markup=kb)
    await message.delete()


# Кнопка Статистика
@dp.message_handler(Text(equals='📊Статистика'))
async def send_statistic(message: types.Message) -> None:
    await message.answer(text="☑️Выбери нужную статистику", reply_markup=kb_statistic)
    await message.delete()


# Кнопка Помощь
@dp.message_handler(Text(equals='🆘Помощь'))
async def send_help(message: types.Message) -> None:
    await message.answer(
        text=HELP_MESSAGE,
        parse_mode="HTML",
        reply_markup=kb
    )


# Кнопка Установить лимит
@dp.message_handler(Text(equals='🌡️Установить лимит'))
async def send_limit(message: types.Message) -> None:
    await message.answer(text=LIMIT_MESSAGE, reply_markup=kb_main)
    await message.delete()


# Установка лимита на расходы
@dp.message_handler(lambda message: Filter.is_handler_limit(message.text))
async def set_limit(message: types.Message) -> None:
    data = LimitData(message.text)
    await message.reply(text=f'✅Лимит установлен на {data.limit} руб. в {data.time}.',
                        reply_markup=kb
                        )


# Сохранение затрат
@dp.message_handler(lambda message: Filter.is_handler_cost(message.text))
async def set_cost(message: types.Message) -> None:
    data = CostData(message.text)
    text = get_cost_message(data)
    await message.reply(text=text, reply_markup=kb)


@dp.message_handler(content_types=types.ContentType.ANY)
async def do_echo(message: types.Message) -> None:
    text = BAD_TEXT_MESSAGE if message.text else NOT_TEXT_MESSAGE
    await message.reply(text=text, reply_markup=kb)


# Обработка исключения при ответе бота при его блокировке
@dp.errors_handler(exception=BotBlocked)
async def err_bot_blocked_handler(update: types.Update, exception: BotBlocked) -> bool:
    return True


# опрашивает сервер
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
