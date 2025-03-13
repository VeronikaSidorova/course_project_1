import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import (calculate_cashback, get_currency_rates, get_greeting, get_top_transactions, process_cards,
                       reader_excel)


def test_get_greeting():  # type: ignore
    assert get_greeting(datetime(2022, 1, 1, 6)) == "Доброе утро!"
    assert get_greeting(datetime(2022, 1, 1, 13)) == "Добрый день!"
    assert get_greeting(datetime(2022, 1, 1, 19)) == "Добрый вечер!"
    assert get_greeting(datetime(2022, 1, 1, 23)) == "Доброй ночи!"


def test_calculate_cashback():  # type: ignore
    assert calculate_cashback(100.0) == 1.0
    assert calculate_cashback(250.50) == 2.505
    assert calculate_cashback(0) == 0.0


def test_process_cards():  # type: ignore
    transactions = [
        {"Номер карты": "1234567890123456", "Сумма операции": 100},
        {"Номер карты": "1234567890123456", "Сумма операции": 50},
        {"Номер карты": "6543210987654321", "Сумма операции": 300},
    ]
    result = process_cards(transactions)
    assert len(result) == 2
    assert result[0]["last_digits"] == "3456"
    assert result[0]["total_spent"] == 150
    assert result[1]["last_digits"] == "4321"
    assert result[1]["total_spent"] == 300


def test_get_top_transactions():  # type: ignore
    transactions = [
        {"Дата операции": "2022-01-01", "Сумма операции": 100, "Категория": "Food", "Описание": "Lunch"},
        {"Дата операции": "2022-01-01", "Сумма операции": 200, "Категория": "Travel", "Описание": "Taxi"},
        {"Дата операции": "2022-01-01", "Сумма операции": 50, "Категория": "Food", "Описание": "Coffee"},
    ]
    result = get_top_transactions(transactions, top_n=2)
    assert len(result) == 2
    assert result[0]["amount"] == 200
    assert result[1]["amount"] == 100


@patch("src.utils.requests.get")
def test_get_currency_rates(mock_get):  # type: ignore
    # Создаем фиктивные данные, которые API мог бы вернуть
    mock_response = MagicMock()
    mock_response.json.return_value = {"Valute": {"USD": {"Value": 74.15}, "EUR": {"Value": 88.25}}}
    mock_get.return_value = mock_response

    # Создаем фиктивные настройки пользователя для теста
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
            {"user_currencies": ["USD", "EUR"]}
        )

        result = get_currency_rates()
        assert len(result) == 2
        assert result[0]["currency"] == "USD"
        assert result[0]["rate"] == 74.15
        assert result[1]["currency"] == "EUR"
        assert result[1]["rate"] == 88.25


@patch("pandas.read_excel")
def test_reader_excel(mock_read_excel):  # type: ignore
    # Настраиваем мок, чтобы он возвращал DataFrame
    mock_read_excel.return_value = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})

    expected = [{"column1": 1, "column2": "a"}, {"column1": 2, "column2": "b"}, {"column1": 3, "column2": "c"}]

    result = reader_excel("test.xlsx")
    assert result == expected
