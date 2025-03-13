import json
import logging

from src.utils import transactions

# Настройки логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_transactions(query: str) -> json:
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми
    транзакциями, содержащими запрос в описании или категории."""
    # Приводим запрос к нижнему регистру
    transactions_l = transactions
    query = query.lower()
    result = []

    # Ищем транзакции
    for transaction in transactions_l:
        description = str(transaction.get("Описание", "")).lower()
        category = str(transaction.get("Категория", "")).lower()

        # Проверяем, содержится ли запрос в описании или категории
        if query in description or query in category:
            result.append(transaction)

    # Логируем количество найденных транзакций
    logger.info(f"Найдено транзакций: {len(result)} по запросу: '{query}'")

    # Возвращаем результат в формате JSON
    return json.dumps(result, ensure_ascii=False, indent=4)
