"""Вспомогательные объекты для взаимодействия с БД"""


from aiogram import types

from keyboards import kb, kb_main
from messages import get_start_message, PROBLEM_MESSAGE, get_limit_massage, get_done_limit_message
from sqlite import is_user_db, get_limits_db, set_limits_db
from utils import LimitData


async def db_is_ready(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    f_name = message.from_user.first_name
    await is_user_db(user_id)
    await message.answer(
        text=get_start_message(f_name),
        parse_mode="HTML",
        reply_markup=kb
    )


async def get_limit(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    try:
        limit_data = await get_limits_db(user_id)
        await message.answer(text=get_limit_massage(limit_data), reply_markup=kb_main)
    except:
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)


async def set_limit(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    data = LimitData(message.text)
    try:
        await set_limits_db(user_id, data)
        await message.reply(text=get_done_limit_message(data),
                            reply_markup=kb
                            )
    except:
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)
