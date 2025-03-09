import json
from datetime import datetime
from typing import Any

import pandas as pd

from views import get_currency_rates, get_greeting, get_stock_prices, get_top_transactions, process_cards


def main(date_time_str, transactions):
    current_time = datetime.now()
    greeting = get_greeting(current_time)

    cards = process_cards(transactions)
    top_transactions = get_top_transactions(transactions)
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


def reader_excel(file_excel: Any) -> list[dict]:
    """Функция для считывания финансовых операций из Excel принимает путь
    к файлу Excel в качестве аргумента и выдает список словарей с транзакциями"""
    transactions_from_excel = pd.read_excel(file_excel, na_filter=True)
    transactions_from_excel.fillna(value=0, inplace=True)
    transactions_from_excel_list = transactions_from_excel.to_dict(orient="records")
    return transactions_from_excel_list


date_time_str = "2023-10-01 14:30:00"
transactions = reader_excel("/Users/veronikasidorova/course_project_1/data/operations.xlsx")


if __name__ == "__main__":
    print(main(date_time_str, transactions))
