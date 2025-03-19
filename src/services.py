import json
import logging

from src.utils import reader_excel

# Настройки логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_transactions(query: str) -> str:
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми
    транзакциями, содержащими запрос в описании или категории."""
    transactions_l = reader_excel()
    # Приводим запрос к нижнему регистру
    query = query.lower()

    # Ищем транзакции
    filtered_df = transactions_l[
        transactions_l["Описание"].str.lower().str.contains(query)
        | transactions_l["Категория"].str.lower().str.contains(query)
    ]

    # Логируем количество найденных транзакций
    logger.info(f"Найдено транзакций: {len(filtered_df)} по запросу: '{query}'")
    result = filtered_df.to_dict(orient="records")

    return json.dumps(result, ensure_ascii=False, indent=4)
