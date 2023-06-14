"""Вспомогательные объекты для взаимодействия с БД"""

import logging
from aiogram import types

from keyboards import kb, kb_main
from messages import get_start_message, PROBLEM_MESSAGE, get_limit_massage, get_done_limit_message, \
    get_done_cost_message, get_cost_massage, BAD_TEXT_MESSAGE
from sqlite import is_user_db, get_limits_db, set_limits_db, set_costs_db, del_cost_db, is_cost_db, \
    del_more_year_cost_db, get_statistic_db
from utils import LimitData, CostData, get_parse_cost, STATISTIC_TIME


async def db_is_ready(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    f_name = message.from_user.first_name
    await del_more_year_cost_db()
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
        await message.answer(text=get_limit_massage(limit_data),
                             parse_mode="HTML",
                             reply_markup=kb_main)
    except Exception:
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)


async def set_limit(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    data = LimitData(message.text)
    try:
        await set_limits_db(user_id, data)
        await message.reply(text=get_done_limit_message(data),
                            reply_markup=kb
                            )
    except Exception:
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)


async def set_cost(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    data = CostData(message.text)
    try:
        await set_costs_db(user_id, data)
        await message.reply(text=get_done_cost_message(data),
                            reply_markup=kb)
    except Exception:
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)


async def get_statistic(message: types.Message) -> None:
    user_id = int(message.from_user.id)
    time = STATISTIC_TIME[message.text]
    try:
        limit_data = await get_limits_db(user_id)
        query_val = await get_statistic_db(user_id, time)
        list_value, total, limit = get_parse_cost(query_val, limit_data, time)
        await message.answer(text=get_cost_massage(list_value, total, limit, time), reply_markup=kb_main)
    except Exception:
        logging.exception("Ошибка в отправке статистики")
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)


async def del_cost(message: types.Message) -> None:
    cost_id = int(message.text[4:])
    cost = await is_cost_db(cost_id)
    if cost:
        try:
            await del_cost_db(cost_id)
            await message.answer(text='✅Успешно удалено!✅', reply_markup=kb_main)
        except Exception:
            await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)
    else:
        await message.answer(text=BAD_TEXT_MESSAGE, reply_markup=kb)
