"""Вспомогательные объекты"""


# ВСПОМОГАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ
LIMIT_TIME = ('день', 'месяц', 'год')
CATEGORY = [
    'бенз',
    'мойка',
    'то',
    'ремонт',
    'шины',
    'аксессуры',
    'прочее'
]


# Класс для получения данных из сообщения для лимита
class LimitData:
    def __init__(self, message: str):
        self.limit, self.time = self.get_kwargs(message)

    def get_kwargs(self, message: str) -> tuple:
        text = message.split()
        return text[0], text[1]


# Класс для получения данных из сообщения для затрат
class CostData:
    def __init__(self, message: str):
        if len(message.split()) == 2:
            self.cost, self.cat = self.get_kwargs(message)
        else:
            self.cost, self.desc, self.cat = self.get_kwargs(message)

    def get_kwargs(self, message: str) -> tuple:
        text = message.split()
        if len(text) == 2:
            return text[0], text[1]
        else:
            cost = text.pop(0)
            cat = text.pop()
            desc = ' '.join(text).replace("(", "").replace(")", "").strip()
            return cost, desc, cat


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
        if len(text) > 2 and text[0].isdecimal() and text[-1] in CATEGORY[3:]:
            return True
        return False
