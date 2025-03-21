import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import get_currency_rates, get_greeting, get_top_transactions, process_cards


def test_get_greeting():  # type: ignore
    assert get_greeting(datetime(2022, 1, 1, 6)) == "Доброе утро!"
    assert get_greeting(datetime(2022, 1, 1, 13)) == "Добрый день!"
    assert get_greeting(datetime(2022, 1, 1, 19)) == "Добрый вечер!"
    assert get_greeting(datetime(2022, 1, 1, 23)) == "Доброй ночи!"


def test_process_cards():  # type: ignore
    # Создаем тестовый DataFrame
    data = {
        "Номер карты": [
            "1234567890123456",
            "1234567890123456",
            "9876543210123456",
            "9876543210123456",
            "1234567890123456",
        ],
        "Сумма операции": [1000, 2000, 1500, 500, 300],
    }
    transactions_card = pd.DataFrame(data)

    # Ожидаемый результат
    expected_result = [{"cashback": 53, "last_digits": "3456", "total_spent": 5300}]

    # Вызов тестируемой функции
    result = process_cards(transactions_card)

    # Проверка результата
    assert result == expected_result, f"Ошибка: ожидалось {expected_result}, получено {result}"


def test_get_top_transactions():  # type: ignore
    data = {
        "Дата платежа": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06"],
        "Сумма операции": [1000, 500, 1500, 2000, 750, 300],
        "Категория": ["Еда", "Транспорт", "Развлечения", "Еда", "Транспорт", "Развлечения"],
        "Описание": ["Покупка еды", "Оплата проезда", "Билет в кино", "Ужин в ресторане", "Такси", "Концерт"],
    }
    transactions_top = pd.DataFrame(data)

    # Ожидаемый результат
    expected_result = [
        {"amount": 2000, "category": "Еда", "date": "2023-10-04", "description": "Ужин в ресторане"},
        {"amount": 1500, "category": "Развлечения", "date": "2023-10-03", "description": "Билет в кино"},
        {"amount": 1000, "category": "Еда", "date": "2023-10-01", "description": "Покупка еды"},
        {"amount": 750, "category": "Транспорт", "date": "2023-10-05", "description": "Такси"},
        {"amount": 500, "category": "Транспорт", "date": "2023-10-02", "description": "Оплата проезда"},
    ]

    # Вызов тестируемой функции
    result = get_top_transactions(transactions_top, top_n=5)

    # Проверка результата
    assert result == expected_result, f"Ошибка: ожидалось {expected_result}, получено {result}"


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
