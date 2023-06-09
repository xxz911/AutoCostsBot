"""Пользовательские сключения"""


# Исключение для невалидного сообщения
class NotValidMessageException(Exception):
    pass


# Исключение для работы с БД
class DataBaseException(Exception):
    pass
