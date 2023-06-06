import logging
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
# logging.basicConfig(level=logging.INFO)

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


# Кнопка главного меню
@dp.message_handler(Text(equals='Главное меню'))
async def send_main(message: types.Message) -> None:
    await message.answer(
        text="📝Напиши мне свои расходы",
        reply_markup=kb
    )
    await message.delete()


# Кнопка Статистика
@dp.message_handler(Text(equals='📊Статистика'))
async def send_statistic(message: types.Message) -> None:
    await message.answer(
        text="☑️Выбери нужную статистику",
        reply_markup=kb_statistic
    )
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
    await message.answer(
        text="📝Напиши сумму и период лимита(день, месяц, год)\n"
             "Пример: 10000 месяц",
        parse_mode="HTML",
        reply_markup=kb_main
    )
    await message.delete()


# Установка лимита на расходы
@dp.message_handler(lambda message: message.text.split()[-1] in ('день', 'месяц', 'год'))  # временное решение с lambda
async def set_limit(message: types.Message) -> None:
    try:
        data = LimitData(message.text)
        await message.answer(text=f'✅Лимит установлен на {data.limit} руб. в {data.time}.',
                             reply_markup=kb,
                             )
    except NotValidMessageException as N:
        await message.answer(text=f'{N.__str__()}\n'
                                  f'📝Попробуй еще раз!',
                             reply_markup=kb_main,
                             )


# Пока что эхо ответ
# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def do_echo(message: types.Message) -> None:
#     await message.reply(
#         text='❤️',
#         reply_markup=kb
#     )


# Обработка исключения при ответе бота при его блокировке
@dp.errors_handler(exception=BotBlocked)
async def err_bot_blocked_handler(update: types.Update, exception: BotBlocked) -> bool:
    print("_____________block________________")
    return True


# опрашивает сервер
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
