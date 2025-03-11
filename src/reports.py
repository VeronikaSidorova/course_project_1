import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

from main import transactions

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def report_decorator(filename: Optional[str] = None):
    if filename is None:
        filename = "report.json"  # Название файла по умолчанию

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)  # Вызов функции и получение результата

            # Запись результата в файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)  # Сохраняем в формате JSON

            logging.info(f"Report saved to {filename}")
            return result

        return wrapper

    return decorator if filename else report_decorator(filename)


@report_decorator()
def spending_by_category(transact_data: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    # Получаем текущую дату, если date не предоставлена
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    # Определяем дату три месяца назад
    three_months_ago = date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transact_data[
        (transact_data['Категория'] == category) &
        (pd.to_datetime(transact_data['Дата операции'], dayfirst=True) >= three_months_ago) &
        (pd.to_datetime(transact_data['Дата операции'], dayfirst=True) <= date)
        ]

    # Суммируем траты
    total_spent = filtered_transactions['Сумма платежа'].sum()


    return total_spent

transactions_df = pd.DataFrame(transactions)
# print(spending_by_category(transactions_df, "Аптеки", "06.01.2020"))
# print(transactions_df[["Категория", "Дата операции"]])



