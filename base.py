import logging
from aiogram import Bot, Dispatcher, executor, types

# Указываем токен
API_TOKEN = ''

# Включаем логирование
logging.basicConfig(level=logging.DEBUG)

# Инициализируем бота и dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Вывод помощи
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        text='''
Мои команды:
/help -- увидеть это сообщение
''',
        reply=False)


# Вывод приветствия
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        text='''
Привет!     
Я бот, который поможет тебе контролировать и анализировать расходы на авто.

Пример ввода расходов: 2500 бенз
''',
        reply=False)
    await send_help(message=message)


# Пока что эхо ответ
@dp.message_handler(content_types=types.ContentType.TEXT)
async def do_echo(message: types.Message):
    text = message.text
    if text and isinstance(text, str) and not text.startswith('/'):
        await message.reply(text=text)

# опрашивает сервер
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
