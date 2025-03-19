import json

from src.services import search_transactions


def test_search_transactions():  # type: ignore
    # Тестируем поиск по описанию
    query = "Apteka 78-439"
    expected_result = [
        {
            "MCC": 5912.0,
            "Бонусы (включая кэшбэк)": 4,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "21.11.2020 17:01:07",
            "Дата платежа": "24.11.2020",
            "Категория": "Аптеки",
            "Кэшбэк": 4.0,
            "Номер карты": "*4556",
            "Округление на инвесткопилку": 0,
            "Описание": "Apteka 78-439",
            "Статус": "OK",
            "Сумма операции": -95.0,
            "Сумма операции с округлением": 95.0,
            "Сумма платежа": -95.0,
        }
    ]
    result = search_transactions(query)
    assert json.loads(result) == expected_result, f"Ошибка: ожидалось {expected_result}, получено {json.loads(result)}"

    # Тестируем поиск, который не дает результатов
    query = "неизвестный запрос"
    expected_result = []
    result = search_transactions(query)
    assert json.loads(result) == expected_result, f"Ошибка: ожидалось {expected_result}, получено {json.loads(result)}"
