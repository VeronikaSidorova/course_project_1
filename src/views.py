from collections import defaultdict

import requests


def get_greeting(current_time):
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def calculate_cashback(total_spent):
    return total_spent / 100


def process_cards(transactions):
    card_data = defaultdict(lambda: {"total_spent": 0, "transactions": []})

    for transaction in transactions:
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


def get_top_transactions(transactions, top_n=5):
    sorted_transactions = sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)
    top_sorted = sorted_transactions[:top_n]
    for_json = []
    for transact in top_sorted:
        date = transact["Дата операции"]
        amount = transact["Сумма операции"]
        category = transact["Категория"]
        description = transact["Описание"]
        for_json.append({"date": date, "amount": amount, "category": category, "description": description})
    return for_json


def get_currency_rates():
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    data_usd = data["Valute"]["USD"]["Value"]
    data_eur = data["Valute"]["EUR"]["Value"]
    return [{"currency": "USD", "rate": data_usd}, {"currency": "EUR", "rate": data_eur}]


def get_stock_prices():
    # Пример фиксированных цен акций
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08},
    ]
