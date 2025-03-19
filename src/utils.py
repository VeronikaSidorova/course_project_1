import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_date_transact(date_in: str) -> pd.DataFrame:
    """Функция? которая возвращает DataFrame, отфильтрованный по дате"""
    # Преобразуйте входную строку на случай, если время отсутствует
    if len(date_in) == 10:  # формат 'DD.MM.YYYY'
        date_in += " 00:00:00"
        logging.debug(f"Преобразована строка даты: {date_in}")
    parsed_date = datetime.strptime(date_in, "%d.%m.%Y %H:%M:%S")
    logging.debug(f"Разобранная дата: {parsed_date}")
    start_date = parsed_date.replace(day=1)
    transact_for_date = reader_excel()
    filter_transact = transact_for_date[
        (pd.to_datetime(transact_for_date["Дата операции"], dayfirst=True) >= start_date)
        & (pd.to_datetime(transact_for_date["Дата операции"], dayfirst=True) <= parsed_date)
    ]
    return filter_transact


def get_greeting(current_time: datetime) -> str:
    """Приветствие в формате "???", где ???
    — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени."""
    logger.info("Получаем текущее время")
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def process_cards(transactions_card: pd.DataFrame) -> List[Dict]:
    """По каждой карте: последние 4 цифры карты; общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""
    transactions_card["last_digits"] = transactions_card["Номер карты"].astype(str).str[-4:]
    total_spent = transactions_card.groupby("last_digits")["Сумма операции"].sum().abs().reset_index().round(2)
    total_spent.rename(columns={"Сумма операции": "total_spent"}, inplace=True)
    total_spent["cashback"] = (total_spent["total_spent"] / 100).astype(int).abs()
    cards = total_spent.to_dict(orient="records")
    logger.info("Получаем данные по картам")
    return cards


def get_top_transactions(transactions_top: pd.DataFrame, top_n: int = 5) -> List[Dict]:
    """Топ-5 транзакций по сумме платежа."""
    sorted_transactions = transactions_top.nlargest(top_n, "Сумма операции")
    result_top = sorted_transactions[["Дата платежа", "Сумма операции", "Категория", "Описание"]].copy()
    result_top.rename(
        columns={
            "Дата платежа": "date",
            "Сумма операции": "amount",
            "Категория": "category",
            "Описание": "description",
        },
        inplace=True,
    )
    result = result_top.to_dict(orient="records")
    logger.info("Получаем данные по топ-5 сумм платежей")
    return result


def get_currency_rates() -> List[Dict[str, Any]]:
    """Курс валют."""
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    data_result = []
    # Определяем путь к файлу user_settings.json относительно текущего скрипта
    settings_path = Path(__file__).parent.parent / "data" / "user_settings.json"
    with open(settings_path) as f:
        currency = json.load(f)
    for cur in currency["user_currencies"]:
        currency_rate = {"currency": cur, "rate": data["Valute"][cur]["Value"]}
        data_result.append(currency_rate)
        logger.info("Получаем данные по курсу валют")
    return data_result


def get_stock_prices() -> List[Dict[str, Any]]:
    """Стоимость акций из S&P500."""
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    date_yesterday = datetime.now() - timedelta(days=1)
    three_days_ago = datetime.now() - timedelta(days=3)
    stop_date = date_yesterday.strftime("%Y-%m-%d")
    start_date = three_days_ago.strftime("%Y-%m-%d")
    headers = {"apikey": API_KEY}
    result = []
    settings_path = Path(__file__).parent.parent / "data" / "user_settings.json"
    with open(settings_path) as f:
        stocks = json.load(f)
    for stock in stocks["user_stocks"]:
        url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{start_date}/{stop_date}?apiKey={API_KEY}"
        response = requests.get(url, headers=headers)
        price = response.json()["results"][0]["c"]
        stock_price = {"stock": stock, "price": price}
        result.append(stock_price)
        logger.info("Получаем данные по стоимости акций")
    return result


def reader_excel() -> pd.DataFrame:
    # формируем путь до таблицы
    logger.info("Получаем датафрейм из xlsx-файла")
    current_dir = os.path.dirname(__file__)
    excel_file_path = os.path.join(current_dir, "..", "data", "operations.xlsx")
    # считываем датафрейм
    transactions_hp = pd.read_excel(excel_file_path)
    return transactions_hp
