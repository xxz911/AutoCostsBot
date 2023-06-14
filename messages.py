"""Сообщения для пользователей"""

from utils import CostData, get_time_is_year, LimitData

BAD_TEXT_MESSAGE = '❌Неправильный текст сообщения❌'
NOT_TEXT_MESSAGE = '❌Нужен только текст❌'
PROBLEM_MESSAGE = '❌Технический сбой, попробуйте позже❌'
HELP_MESSAGE = '''
‼️<b>РАСХОД</b> пишется <b>С МАЛЕНЬКОЙ БУКВЫ</b> и в <b>ОДНУ</b> из категорий:

<b>🔹бензин🔹мойка🔺то🔺ремонт🔺шины🔺аксессуары🔺прочее🔺</b>

‼️Для <b>ВСЕХ</b> категорий <b>КРОМЕ 🔹бензин🔹мойка🔹</b> указывается <b>ОПИСАНИЕ</b>

⚠️<b>Для бензин мойка</b>⚠️
Сумма категория:
<em>Пример: 2500 бензин</em>

⚠️<b>Для остальных</b>⚠️
Суммa описание категория:
<em>Пример: 3000 муфта, правка диска ремонт</em>
'''


def get_done_limit_message(data: LimitData) -> str:
    return f'✅Лимит установлен на {data.limit} руб. в {data.time}.'


def get_start_message(user: str) -> str:
    return f'<em><b>{user}, 🎉 Добро пожаловать! 🎉</b></em>\n' \
           f'<em>Я 🤖, который поможет тебе анализировать расходы на авто!</em>'


def get_limit_massage(limit_data: tuple) -> str:
    limit_day = 'ОТСУТСТВУЕТ' if limit_data[0] == 0 else f'{limit_data[0]} руб.'
    limit_month = 'ОТСУТСТВУЕТ' if limit_data[1] == 0 else f'{limit_data[1]} руб.'
    limit_year = 'ОТСУТСТВУЕТ' if limit_data[2] == 0 else f'{limit_data[2]} руб.'
    return f'''
<em>🌡<b>Установленные лимиты:</b>🌡

🔸На день: {limit_day} 
🔸На месяц: {limit_month} 
🔸На год: {limit_year} 

📝Напиши <b>сумму</b> и период(<b>день, месяц, год</b>) лимита
Пример: 10000 месяц</em>
'''


def get_done_cost_message(data: CostData) -> str:
    data.cat = data.cat.upper()
    if hasattr(data, 'desc'):
        return f'Расход: {data.cost} руб. {data.desc} в категорию {data.cat}\n' \
               f'✅СОХРАНЕН!✅'
    else:
        return f'Расход: {data.cost} руб. на {data.cat}\n' \
               f'✅СОХРАНЕН!✅'


# Функция для формирования базового текста для вывода статистики
def get_text_cost(limit: int, time: str, total: int) -> str:
    is_limit = False if limit == 'ОТСУТСТВУЕТ' else True
    time_is_year = get_time_is_year(time)
    time = time.upper()
    balance = limit - total
    limit = 'ОТСУТСТВУЕТ' if not limit else f'{limit} руб.'

    if time_is_year:
        text = f'\n🌡Лимит: {limit} за {time}🌡\n' \
               f'🧮Итог: {total} руб. за {time}🧮\n'
    else:
        text = f'🗑(del) - удалить расход🗑\n' \
               f'🧮Итог: {total} руб. за {time}🧮\n' \
               f'🌡Лимит: {limit} за {time}🌡\n'
    if is_limit:
        if balance >= 0:
            text += f'🟢Меньше лимита: {balance} руб.🟢\n\n'
        else:
            text += f'🔴Больше лимита: {abs(balance)} руб.🔴\n\n'
    return text


# Функция для формирования текста списка расходов для вывода статистики
def get_text_row(time: str, row: dict) -> str:
    if time.lower() != 'год':
        row["desc"] = '' if row["desc"] == '-' else row["desc"]
        return f'💸{row["cost"]} руб. {row["desc"]} {row["cat"].upper()} {row["date"]}(/del{row["id"]})\n\n'
    else:
        return f'💸{row["sums"]} руб. на {row["cat"].upper()}\n\n'


# Функция для формирования текста для вывода статистики
def get_cost_massage(dict_val: dict, total: int, limit: int, time: str) -> str:
    if dict_val:
        base_text = get_text_cost(limit, time, total)

        if len(dict_val) == 1:
            row = dict_val[0]
            list_costs_text = get_text_row(time, row)
            return list_costs_text + base_text
        else:
            list_costs_text = ''
            for row in dict_val:
                list_costs_text += get_text_row(time, row)
            return list_costs_text + base_text

    limit = 'ОТСУТСТВУЕТ' if not limit else f'{limit} руб.'
    return f'🌡Лимит: {limit} за {time}🌡\n' \
           f'🧮Итог: Нет затрат за {time}🧮'
