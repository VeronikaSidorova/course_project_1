import json

from src.views import home_page


def test_home_page():  # type: ignore
    # Подготовка данных для теста
    date_time_str = "12.02.2020"

    # Вызов тестируемой функции
    result = home_page(date_time_str)

    # Ожидаемый результат
    expected_result = {
        "cards": [
            {"cashback": 15, "last_digits": "4556", "total_spent": 1523.7},
            {"cashback": 203, "last_digits": "7197", "total_spent": 20386.11},
            {"cashback": 4, "last_digits": "nan", "total_spent": 400.0},
        ],
        "currency_rates": [{"currency": "USD", "rate": 82.8487}, {"currency": "EUR", "rate": 90.8257}],
        "greeting": "Добрый вечер!",
        "stock_prices": [
            {"price": 214, "stock": "AAPL"},
            {"price": 195.74, "stock": "AMZN"},
            {"price": 164.29, "stock": "GOOGL"},
            {"price": 388.7, "stock": "MSFT"},
            {"price": 238.01, "stock": "TSLA"},
        ],
        "top_transactions": [
            {"amount": 403.0, "category": "Ж/д билеты", "date": "11.02.2020", "description": "РЖД"},
            {"amount": 300.0, "category": "Переводы", "date": "06.02.2020", "description": "Артем П."},
            {"amount": -25.71, "category": "Супермаркеты", "date": "09.02.2020", "description": "Магнит"},
            {"amount": -34.0, "category": "Супермаркеты", "date": "13.02.2020", "description": "Колхоз"},
            {"amount": -34.22, "category": "Супермаркеты", "date": "05.02.2020", "description": "Магнит"},
        ],
    }

    # Проверка результата
    assert json.loads(result) == expected_result, f"Ошибка: ожидалось {expected_result}, получено {json.loads(result)}"
