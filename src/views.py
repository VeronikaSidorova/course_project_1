import json
import logging
from datetime import datetime

from src.utils import (
    get_currency_rates,
    get_date_transact,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
    process_cards,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def home_page(date_time_str: str) -> str:
    """главная функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающая JSON-ответ с данными"""
    logger.info("Получаем дату и формируем JSON ответ для страницы главная")

    current_time = datetime.now()
    greeting = get_greeting(current_time)
    cards = process_cards(get_date_transact(date_time_str))
    top_transactions = get_top_transactions(get_date_transact(date_time_str))
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()
    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response, ensure_ascii=False, indent=2)
