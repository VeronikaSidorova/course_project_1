import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def report_decorator(filename: Optional[str] = None): # type: ignore
    """декоратор для функций-отчетов, который записывает в файл результат,
    который возвращает функция, формирующая отчет."""
    if filename is None:
        filename = "report.json"  # Название файла по умолчанию

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any: # type: ignore
            result = func(*args, **kwargs)  # Вызов функции и получение результата

            # Запись результата в файл
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)  # Сохраняем в формате JSON

            logging.info(f"Report saved to {filename}")
            return result

        return wrapper

    return decorator if filename else report_decorator(filename)


@report_decorator()
def spending_by_category(transact_data: pd.DataFrame, category: str, date: Optional[str | None] = None) -> int:
    """Функция возвращает траты по заданной категории за последние три месяца
    (от переданной даты)."""
    # Получаем текущую дату, если date не предоставлена
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    # Определяем дату три месяца назад
    three_months_ago = date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    category_filter = category.lower()
    filtered_transactions = transact_data[
        (transact_data["Категория"] == category_filter)
        & (pd.to_datetime(transact_data["Дата операции"], dayfirst=True) >= three_months_ago)
        & (pd.to_datetime(transact_data["Дата операции"], dayfirst=True) <= date)
    ]

    # Суммируем траты
    total_spent = filtered_transactions["Сумма платежа"].sum()

    return total_spent
