"""Запросы к БД"""


import logging
import sqlite3 as sq
from exceptions import DataBaseException
from utils import CATEGORY_DB, LimitData, LIMIT_DB


async def db_create() -> None:
    global db, cur

    db = sq.connect('sqlite.db')
    cur = db.cursor()

    cur.execute("""PRAGMA foreign_keys=on;""")
    cur.execute("""CREATE TABLE IF NOT EXISTS costs(
        costs_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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
    else:
        db.commit()


async def is_user_db(user_id: int) -> None:
    user = cur.execute(f"SELECT user_id from users WHERE user_id = {user_id}").fetchone()
    if not user:
        try:
            cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (user_id, 0, 0, 0))
            db.commit()
        except:
            logging.error("Неизвестная ошибка добавления юзера в БД")
            raise DataBaseException("Неизвестная ошибка добавления юзера в БД")


async def get_limits_db(user_id: int) -> tuple:
    try:
        limits = cur.execute(f"SELECT limit_day, limit_month, limit_year FROM users WHERE user_id = {user_id}")
        return limits.fetchone()
    except:
        logging.error("Неизвестная ошибка получения лимита из БД")
        raise DataBaseException


async def set_limits_db(user_id: int, data: LimitData) -> None:
    time = LIMIT_DB[data.time]
    limit = int(data.limit)

    try:
        cur.execute(f"UPDATE users SET {time} = ? WHERE user_id = ?", (limit, user_id))
        db.commit()
    except:
        logging.error("Неизвестная ошибка изменения лимита из БД")
        raise DataBaseException
