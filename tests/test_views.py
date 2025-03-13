import json

import pytest

from src.utils import transactions
from src.views import home_page

transactions_list = transactions


# Заглушки для функций
def mock_get_greeting(current_time):  # type: ignore
    hour = current_time.hour
    if hour < 6:
        return "Доброй ночи!"
    elif hour < 12:
        return "Доброе утро!"
    elif hour < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


# Тесты
@pytest.fixture
def mock_functions(monkeypatch):  # type: ignore
    monkeypatch.setattr("src.utils.get_greeting", mock_get_greeting)


def test_home_page(mock_functions):  # type: ignore
    date_time_str = "2023-10-01 12:00:00"
    response_json = home_page(date_time_str, transactions_list)
    response = json.loads(response_json)

    # Проверка структуры ответа
    assert "greeting" in response
    assert response["greeting"] == "Добрый вечер!"  # В зависимости от времени
