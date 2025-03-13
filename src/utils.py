import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv


def get_greeting(current_time: datetime) -> str:
    """Приветствие в формате "???", где ???
    — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени."""
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def calculate_cashback(total_spent: float) -> float:
    """кешбэк (1 рубль на каждые 100 рублей)."""
    return total_spent / 100


def process_cards(transactions_card: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """По каждой карте: последние 4 цифры карты; общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""
    card_data = defaultdict(lambda: {"total_spent": 0, "transactions": []}) # type: ignore

    for transaction in transactions_card:
        card_number = str(transaction["Номер карты"])
        amount = transaction["Сумма операции"]

        card_data[card_number]["total_spent"] += amount
        card_data[card_number]["transactions"].append(transaction)

    cards = []
    for card_number, data in card_data.items():
        last_digits = card_number[-4:]
        total_spent = data["total_spent"]
        cashback = calculate_cashback(total_spent)
        cards.append({"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback})

    return cards


def get_top_transactions(transactions_top: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """Топ-5 транзакций по сумме платежа."""
    sorted_transactions = sorted(transactions_top, key=lambda x: x["Сумма операции"], reverse=True)
    top_sorted = sorted_transactions[:top_n]
    for_json = []
    for transact in top_sorted:
        date = transact["Дата операции"]
        amount = transact["Сумма операции"]
        category = transact["Категория"]
        description = transact["Описание"]
        for_json.append({"date": date, "amount": amount, "category": category, "description": description})
    return for_json


def get_currency_rates() -> List[Dict[str, Any]]:
    """Курс валют."""
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    data_result = []
    with open("/Users/veronikasidorova/course_project_1/data/user_settings.json") as f:
        currency = json.load(f)
    for cur in currency["user_currencies"]:
        currency_rate = {"currency": cur, "rate": data["Valute"][cur]["Value"]}
        data_result.append(currency_rate)
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
    with open("/Users/veronikasidorova/course_project_1/data/user_settings.json") as f:
        stocks = json.load(f)
    for stock in stocks["user_stocks"]:
        url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{start_date}/{stop_date}?apiKey={API_KEY}"
        response = requests.get(url, headers=headers)
        price = response.json()["results"][0]["c"]
        stock_price = {"stock": stock, "price": price}
        result.append(stock_price)
    return result


def reader_excel(file_excel: Any) -> list[dict]:
    """Функция для считывания финансовых операций из Excel принимает путь
    к файлу Excel в качестве аргумента и выдает список словарей с транзакциями"""
    transactions_from_excel = pd.read_excel(file_excel, na_filter=True)
    transactions_from_excel.fillna(value=0, inplace=True)
    transactions_from_excel_list = transactions_from_excel.to_dict(orient="records")
    return transactions_from_excel_list


transactions = reader_excel("/Users/veronikasidorova/course_project_1/data/operations.xlsx")
