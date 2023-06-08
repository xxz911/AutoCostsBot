"""Сообщения для пользователей"""

from utils import CostData

BAD_TEXT_MESSAGE = f'❌Неправильный текст сообщения❌'
NOT_TEXT_MESSAGE = f'❌Нужен только текст❌'
LIMIT_MESSAGE = "📝Напиши сумму и период(день, месяц, год) лимита\n" \
                "Пример: 10000 месяц"

HELP_MESSAGE = '''
⚠️Для бензин/мойка⚠️
Напиши сумму и категорию:
Пример: 2500 бензин

⚠️Для то/ремонт/шины/аксессуары/прочее⚠️
Напиши сумму, описание, категорию:
Пример: 3000 муфта и ремень ГРМ то 
'''


def get_start_message(user: str) -> str:
    start_message = \
        f'<em><b>{user}, Добро пожаловать!</b></em>\n'\
        f'<em>Я бот, который поможет тебе анализировать расходы на авто!</em>'
    return start_message


def get_cost_message(data: CostData) -> str:
    if hasattr(data, 'desc'):
        return f'✅ Расходы: {data.cost} руб. на {data.desc} категории {data.cat}\n' \
               f'СОХРАНЕНЫ!'
    else:
        return  f'✅ Расходы: {data.cost} руб. на категорию {data.cat}\n' \
               f'СОХРАНЕНЫ!'
