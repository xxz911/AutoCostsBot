"""Сообщения для пользователей"""

from utils import CostData

BAD_TEXT_MESSAGE = f'❌Неправильный текст сообщения❌'
NOT_TEXT_MESSAGE = f'❌Нужен только текст❌'
PROBLEM_MESSAGE = '❌Технический сбой, попробуйте позже❌'
HELP_MESSAGE = '''
⚠️Для бензин/мойка⚠️
Напиши сумму и категорию:
Пример: 2500 бензин

⚠️Для то/ремонт/шины/аксессуары/прочее⚠️
Напиши сумму, описание, категорию:
Пример: 3000 муфта и ремень ГРМ то 
'''


def get_done_limit_message(data):
    return f'✅Лимит установлен на {data.limit} руб. в {data.time}.'


def get_start_message(user: str) -> str:
    start_message = \
        f'<em><b>{user}, Добро пожаловать!</b></em>\n'\
        f'<em>Я бот, который поможет тебе анализировать расходы на авто!</em>'
    return start_message


def get_limit_massage(limit_data):
    limit_day = 'НЕ УСТАНОВЛЕН' if limit_data[0] == 0 else limit_data[0]
    limit_month = 'НЕ УСТАНОВЛЕН' if limit_data[1] == 0 else limit_data[1]
    limit_year = 'НЕ УСТАНОВЛЕН' if limit_data[2] == 0 else limit_data[2]
    return f'''
Установленные лимиты:

На день: {limit_day}
На месяц: {limit_month}
На год: {limit_year}

📝Напиши сумму и период(день, месяц, год) лимита:
Пример: 10000 месяц
'''


def get_done_cost_message(data: CostData) -> str:
    if hasattr(data, 'desc'):
        return f'✅ Расходы: {data.cost} руб. на {data.desc} категории {data.cat}\n' \
               f'СОХРАНЕНЫ!'
    else:
        return f'✅ Расходы: {data.cost} руб. на категорию {data.cat}\n' \
               f'СОХРАНЕНЫ!'

