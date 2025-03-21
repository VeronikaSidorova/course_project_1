import logging
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def report_decorator(filename: Optional[str] = None):  # type: ignore
    """декоратор для функций-отчетов, который записывает в файл результат,
    который возвращает функция, формирующая отчет."""
    if filename is None:
        filename = "report.json"  # Название файла по умолчанию

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:  # type: ignore
            result = func(*args, **kwargs)  # Вызов функции и получение результата

            logger.info("Проверка: являются ли данные датафреймом")
            if isinstance(result, pd.DataFrame):
                logger.info("Запись отчёта в файл")
                result.to_json(filename, orient="records", lines=True, force_ascii=False)
            else:
                logger.error("Данные не являются датафреймом. В файл записаны не будут")
            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transact_data: pd.DataFrame, category: str, date: datetime | None = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца
    (от переданной даты)."""
    # Получаем текущую дату, если date не предоставлена
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date, format="%d.%m.%Y")

    # Определяем дату три месяца назад
    three_months_ago = date - pd.DateOffset(months=3)

    # Фильтруем транзакции по категории и дате
    category_filter = category.title()

    filtered_transactions = transact_data[
        (transact_data["Сумма операции"] < 0)
        & (transact_data["Категория"] == category_filter)
        & (pd.to_datetime(transact_data["Дата операции"], dayfirst=True) >= three_months_ago)
        & (pd.to_datetime(transact_data["Дата операции"], dayfirst=True) <= date)
    ]

    # Суммируем траты
    total_spent = filtered_transactions["Сумма платежа"].abs().sum()

    logger.info(f"Траты по категории {category} составили {total_spent}")

    return pd.DataFrame({total_spent})
