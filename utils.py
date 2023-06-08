"""Вспомогательные объекты"""


# ВСПОМОГАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ
LIMIT_TIME = ('день', 'месяц', 'год')
CATEGORY = [
    'бензин',
    'мойка',
    'то',
    'ремонт',
    'шины',
    'аксессуары',
    'прочее'
]


# Класс для получения данных из сообщения для лимита
class LimitData:
    def __init__(self, message: str):
        self.limit, self.time = self.get_limit_args(message)

    def get_limit_args(self, message: str) -> tuple:
        text = message.split()
        return int(text[0]), text[1]


# Класс для получения данных из сообщения для затрат
class CostData:
    def __init__(self, message: str):
        if len(message.split()) == 2:
            self.cost, self.cat = self.get_limit_args(message)
        else:
            self.cost, self.desc, self.cat = self.get_limit_args(message)

    def get_limit_args(self, message: str) -> tuple:
        text = message.split()
        if len(text) == 2:
            return int(text[0]), text[1]
        else:
            cost = text.pop(0)
            cat = text.pop()
            desc = ' '.join(text).replace("(", "").replace(")", "").strip()
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
