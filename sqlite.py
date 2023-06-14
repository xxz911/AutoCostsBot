"""Запросы к БД"""

import logging
import sqlite3 as sq

from datetime import datetime
from exceptions import DataBaseException
from utils import CATEGORY_DB, LimitData, LIMIT_DB, CostData, get_dict_time_db


async def db_create() -> None:
    try:
        global db, cur

        db = sq.connect('sqlite.db')
        cur = db.cursor()

        cur.execute("""PRAGMA foreign_keys=on;""")

        cur.execute("""CREATE TABLE IF NOT EXISTS costs(
            cost_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER NOT NULL,
            description NCHAR(55) NOT NULL,
            cost INTEGER NOT NULL,
            cat_id INTEGER NOT NULL,
            create_date DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (cat_id) REFERENCES category(cat_id));""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
           user_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
           limit_day INTEGER DEFAULT (0) NOT NULL,
           limit_month INTEGER DEFAULT (0) NOT NULL,
           limit_year INTEGER DEFAULT (0) NOT NULL);
           """)

        cur.execute("""CREATE TABLE IF NOT EXISTS category(
           cat_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
           name TEXT NOT NULL);""")

        if len(cur.execute("SELECT name FROM category").fetchall()) < 7:
            query = "INSERT INTO category VALUES(?,?)"
            values = [(1, CATEGORY_DB['бензин']),
                      (2, CATEGORY_DB['мойка']),
                      (3, CATEGORY_DB['то']),
                      (4, CATEGORY_DB['ремонт']),
                      (5, CATEGORY_DB['шины']),
                      (6, CATEGORY_DB['аксессуары']),
                      (7, CATEGORY_DB['прочее'])
                      ]
            cur.executemany(query, values)
            db.commit()
    except Exception:
        logging.exception("Ошибка создания БД")
        raise DataBaseException


async def is_user_db(user_id: int) -> None:
    try:
        user = cur.execute("SELECT user_id from users WHERE user_id = ?", (user_id,)).fetchone()
    except Exception:
        logging.exception("Ошибка поиска юзера в БД")
        raise DataBaseException
    if not user:
        try:
            cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (user_id, 0, 0, 0))
            db.commit()
        except Exception:
            logging.exception("Ошибка добавления юзера в БД")
            raise DataBaseException


async def del_more_year_cost_db() -> None:
    start_year = get_dict_time_db()['год'][0]
    try:
        cur.execute("DELETE FROM costs WHERE create_date < (?)", (start_year,))
        db.commit()

    except Exception:
        logging.exception("Ошибка удаления расходов более года в БД")
        raise DataBaseException


async def get_limits_db(user_id: int) -> tuple:
    try:
        limits = cur.execute("SELECT limit_day, limit_month, limit_year FROM users WHERE user_id = ?", (user_id,))
        return limits.fetchone()
    except Exception:
        logging.exception("Ошибка получения лимита из БД")
        raise DataBaseException


async def set_limits_db(user_id: int, data: LimitData) -> None:
    time = LIMIT_DB[data.time]
    limit = int(data.limit)

    try:
        cur.execute(f"UPDATE users SET {time} = ? WHERE user_id = ?", (limit, user_id))
        db.commit()
    except Exception:
        logging.exception("Ошибка изменения лимита из БД")
        raise DataBaseException


async def set_costs_db(user_id: int, data: CostData) -> None:
    try:
        desc = '-' if not hasattr(data, 'desc') else data.desc
        cost = data.cost
        create_time = datetime.now()
        query_cat = cur.execute("SELECT cat_id FROM category WHERE name=?", (CATEGORY_DB[data.cat],)).fetchone()
        cat = int(query_cat[0])
        val = (user_id, desc, cost, cat, create_time)
    except Exception:
        logging.exception("Ошибка получения cat_id из category в запросе к БД")
        raise DataBaseException

    try:
        cur.execute("INSERT INTO costs (user_id, description, cost, cat_id, create_date) VALUES(?, ?, ?, ?, ?)", val)
        db.commit()
    except Exception:
        logging.exception("Ошибка внесения расходов в БД")
        raise DataBaseException


async def get_statistic_db(user_id: int, time: str) -> list:
    try:
        if time != 'год':
            start, end = get_dict_time_db()[time][0], get_dict_time_db()[time][1]
            query = cur.execute(
                f"SELECT cost, description, name, strftime('%H:%M %d.%m', create_date), cost_id FROM costs "
                f"JOIN category ON costs.cat_id=category.cat_id "
                f"WHERE costs.user_id='{user_id}' "
                f"AND create_date between '{start}' and '{end}'"
            )
            return query.fetchall()
        else:
            start, end = get_dict_time_db()[time][0], get_dict_time_db()[time][1]
            query = cur.execute(
                f"SELECT name, sum(cost) as sum FROM costs "
                f"JOIN category ON costs.cat_id=category.cat_id "
                f"WHERE costs.user_id='{user_id}' "
                f"AND create_date between '{start}' and '{end}'"
                f"GROUP BY name"
            )
            return query.fetchall()
    except Exception:
        logging.exception("Ошибка запроса расходов в БД")
        raise DataBaseException


async def is_cost_db(cost_id: int) -> bool:
    try:
        cost = cur.execute("SELECT cost_id from costs WHERE cost_id=?", (cost_id,)).fetchone()
        return True if cost else False
    except Exception:
        logging.exception("Ошибка проверки id расхода в БД")
        raise DataBaseException


async def del_cost_db(cost_id: int) -> None:
    try:
        cur.execute("DELETE FROM costs WHERE cost_id=?", (cost_id,))
        db.commit()
    except Exception:
        logging.exception("Ошибка удаления расхода из БД")
        raise DataBaseException
