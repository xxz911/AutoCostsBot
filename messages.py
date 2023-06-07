"""Сообщения для пользователей"""

from utils import CostData

BAD_TEXT_MESSAGE = f'❌Неправильный текст сообщения❌'
NOT_TEXT_MESSAGE = f'❌Нужен только текст❌'
LIMIT_MESSAGE = "📝Напиши сумму и период(день, месяц, год) лимита\n" \
                "Пример: 10000 месяц"

HELP_MESSAGE = '''
<em><b>Пример ввода расходов:</b></em>

⚠️<em>Без описания трат:</em>
2500 <b>бензин</b>
600 <b>мойка</b>

⚠️<em>С описанием в скобках трат:</em>
3000 (малое) <b>то</b>
9000 (рычаги и генератор) <b>ремонт</b>
25000 (летняя Кама) <b>шины</b>
30000 (коврики) <b>аксессуры</b>
5000 (полировка) <b>прочее</b>
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
