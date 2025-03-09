from unittest.mock import patch

from src.views import get_greeting


@patch()
def test_get_greetings(mock_datetime):
    mock_datetime.now.return_value.hour = 10
    assert get_greeting() == "Доброе утро"
    mock_datetime.now.return_value.hour = 15
    assert get_greeting() == "Добрый день"
    mock_datetime.now.return_value.hour = 20
    assert get_greeting() == "Добрый вечер"
    mock_datetime.now.return_value.hour = 23
    assert get_greeting() == "Доброй ночи"
