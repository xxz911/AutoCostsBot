"""Тесты"""


import pytest

from utils import CostData, LimitData, Filter


# Тест парсинга сообщения затрат
@pytest.mark.parametrize("message, expected_result", [
    ('200 бенз', {'cat': 'бенз', 'cost': 200}),
    ('5000 коврики на машину то', {'cat': 'то', 'cost': 5000, 'desc': 'коврики на машину'}),
])
def test_get_cost_args(message: str, expected_result: bool) -> None:
    result = CostData(message).__dict__
    assert result == expected_result


# Тест парсинга сообщения лимита
@pytest.mark.parametrize("message, expected_result", [
    ('200 день', {'limit': 200, 'time': 'день'}),
    ('20000 месяц', {'limit': 20000, 'time': 'месяц'}),
    ('20000000 год', {'limit': 20000000, 'time': 'год'}),
])
def test_get_limit_args(message: str, expected_result: bool) -> None:
    result = LimitData(message).__dict__
    assert result == expected_result


# Тест фильтра hendler на ввод лимита
@pytest.mark.parametrize("message, expected_result", [
    ('200 день', True),
    ('20000 месяц', True),
    ('20000000 год', True),

    ('200 День', False),
    ('200 20 день', False),
    ('20000 2 месяц', False),
    ('20000000 1 год', False),
    ('200 мой день', False),
    ('200 мой общие', False),
])
def test_is_handler_limit(message: str, expected_result: bool) -> None:
    result = Filter.is_handler_limit(message)
    assert result == expected_result


# Тест фильтра hendler на ввод затрат
@pytest.mark.parametrize("message, expected_result", [
    ('200 бензин', True),
    ('600 мойка', True),
    ('5000 коврики на машину то', True),
    ('5000 коврики на машину ремонт', True),
    ('5000 коврики на машину шины', True),
    ('5000 коврики на машину аксессуары', True),
    ('5000 коврики на машину прочее', True),

    ('600 Мойка', False),
    ('5000 коврики на машину ТО', False),
    ('бенз', False),
    ('200', False),
    ('200 бенза', False),
    ('600а мойка', False),

])
def test_is_handler_cost(message: str, expected_result: bool) -> None:
    result = Filter.is_handler_cost(message)
    assert result == expected_result
