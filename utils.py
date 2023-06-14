"""Вспомогательные объекты"""

from datetime import datetime, timedelta, date

# ВСПОМОГАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ
LIMIT_TIME = ('день', 'месяц', 'год')
CATEGORY_DB = {
    'бензин': 'fuel',
    'мойка': 'wash',
    'то': 'to',
    'ремонт': 'repair',
    'шины': 'tires',
    'аксессуары': 'accessories',
    'прочее': 'other'
}
RUS_CATEGORY_DB = {
    'fuel': 'Бензин',
    'wash': 'Мойка',
    'to': 'Tо',
    'repair': 'Ремонт',
    'tires': 'Шины',
    'accessories': 'Аксессуары',
    'other': 'Прочее'
}
CATEGORY = list(CATEGORY_DB)
LIMIT_DB = {
    'день': 'limit_day',
    'месяц': 'limit_month',
    'год': 'limit_year',
}
STATISTIC_TIME = {
    '📜 Дневная': 'день',
    '📜 Месячная': 'месяц',
    '📜 Годовая': 'год',
}


# Функция для формирования словаря статистики с временем для запросов
def get_dict_time_db() -> dict:
    date_today = datetime.date(datetime.now())
    start_day = datetime.combine(date.today(), datetime.min.time())
    end_day = datetime.combine(date.today(), datetime.max.time())
    start_month = datetime.now().replace(day=1, hour=0, minute=0)
    end_month = datetime.combine(
        date_today.replace(day=28) + timedelta(days=4) - timedelta(days=4),
        datetime.max.time()
    )
    start_year = datetime.now().replace(month=1, day=1, hour=0, minute=0)
    end_year = datetime.combine(
        date_today.replace(month=12, day=31) + timedelta(days=4) - timedelta(days=4),
        datetime.max.time()
    )

    return {
        'день': (start_day, end_day),
        'месяц': (start_month, end_month),
        'год': (start_year, end_year),
    }


# Класс для получения данных из сообщения для лимитов
class LimitData:
    def __init__(self, message: str):
        self.limit, self.time = self.get_limit_args(message)

    @staticmethod
    def get_limit_args(message: str) -> tuple:
        text = message.split()
        return int(text[0]), text[1]


# Класс для получения данных из сообщения для затрат
class CostData:
    def __init__(self, message: str):
        if len(message.split()) == 2:
            self.cost, self.cat = self.get_cost_args(message)
        else:
            self.cost, self.desc, self.cat = self.get_cost_args(message)

    @staticmethod
    def get_cost_args(message: str) -> tuple:
        text = message.split()
        if len(text) == 2:
            return int(text[0]), text[1]
        else:
            cost = text.pop(0)
            cat = text.pop()
            desc = ' '.join(text).strip()
            return int(cost), desc, cat


# Класс фильтра хендлера
class Filter:
    @staticmethod
    def is_handler_limit(message: str) -> bool:
        text = message.split()
        if len(text) == 2 and text[0].isdecimal() and text[1] in LIMIT_TIME:
            return True
        return False

    @staticmethod
    def is_handler_cost(message: str) -> bool:
        text = message.split()
        if len(text) == 2 and text[1] in CATEGORY[:2] and text[0].isdecimal():
            return True
        if len(text) > 2 and text[0].isdecimal() and text[-1] in CATEGORY[2:]:
            return True
        return False


# Функция для проверки является ли время годом
def get_time_is_year(time: str) -> bool:
    return True if time.lower() == 'год' else False


# Функция для формирования переменных для функции парсинга запроса из бд
def get_const(limit_data: tuple, time: str) -> tuple:
    if time == 'день':
        limit = limit_data[0]
    elif time == 'месяц':
        limit = limit_data[1]
    else:
        limit = limit_data[2]

    fields = ['cat', 'sums'] if time == 'год' else ['cost', 'desc', 'cat', 'date', 'id']
    time_is_year = get_time_is_year(time)

    return fields, limit, time_is_year


# Функция для формирования словаря из данных запроса бд
def get_row_val(fields: list, time_is_year: bool, row: dict) -> dict:
    dict_value = {}
    for index, column in enumerate(fields):
        if time_is_year and index == 0 or (not time_is_year) and index == 2:
            dict_value[column] = RUS_CATEGORY_DB[row[index]]
        else:
            dict_value[column] = row[index]
    return dict_value


# Функция для формирования суммы расходов
def get_total_cost(query_res: list, list_value: list, time_is_year: bool) -> list:
    if len(query_res) == 1:
        return list_value[0]['sums'] if time_is_year else list_value[0]['cost']
    if time_is_year:
        return sum([key['sums'] for key in list_value])
    else:
        return sum([key['cost'] for key in list_value])


# Функция парсинга данных из бд запроса
def get_parse_cost(query_res: list, limit_data: tuple, time: str) -> tuple:
    fields, limit, time_is_year = get_const(limit_data, time)
    list_value = []

    if query_res:
        if len(query_res) == 1:
            row = query_res[0]
            list_value.append(get_row_val(fields, time_is_year, row))
            total_cost = get_total_cost(query_res, list_value, time_is_year)
            return list_value, total_cost, limit
        else:
            for row in query_res:
                list_value.append(get_row_val(fields, time_is_year, row))
            total_cost = get_total_cost(query_res, list_value, time_is_year)
            return list_value, total_cost, limit

    return query_res, 0, limit
