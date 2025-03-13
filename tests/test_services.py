import json
import unittest

from src.services import search_transactions


class TestSearchTransactions(unittest.TestCase):  # type: ignore

    def setUp(self):  # type: ignore
        # Подготовка тестовых данных
        self.transactions = [
            {"ID": 1, "Описание": "Покупка кофе", "Категория": "Еда", "Сумма": 5.0},
            {"ID": 2, "Описание": "Оплата коммунальных услуг", "Категория": "Коммуналка", "Сумма": 100.0},
            {"ID": 3, "Описание": "Купил новый компьютер", "Категория": "Электроника", "Сумма": 1500.0},
            {"ID": 4, "Описание": "Посещение кинотеатра", "Категория": "Развлечения", "Сумма": 15.0},
        ]

    def test_search_by_description(self):  # type: ignore
        result = search_transactions(self.transactions, "кофе")
        expected = [{"ID": 1, "Описание": "Покупка кофе", "Категория": "Еда", "Сумма": 5.0}]
        self.assertEqual(json.loads(result), expected)

    def test_search_by_category(self):  # type: ignore
        result = search_transactions(self.transactions, "развлечения")
        expected = [{"ID": 4, "Описание": "Посещение кинотеатра", "Категория": "Развлечения", "Сумма": 15.0}]
        self.assertEqual(json.loads(result), expected)

    def test_search_no_matches(self):  # type: ignore
        result = search_transactions(self.transactions, "негативный запрос")
        expected = []
        self.assertEqual(json.loads(result), expected)

    def test_search_empty_query(self):  # type: ignore
        result = search_transactions(self.transactions, "")
        expected = self.transactions  # Ожидаем, что вернется весь список транзакций
        self.assertEqual(json.loads(result), expected)

    def test_search_case_insensitivity(self):  # type: ignore
        result = search_transactions(self.transactions, "КОФЕ")
        expected = [{"ID": 1, "Описание": "Покупка кофе", "Категория": "Еда", "Сумма": 5.0}]
        self.assertEqual(json.loads(result), expected)
