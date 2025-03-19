import unittest

import pandas as pd

from src.reports import spending_by_category


class TestSpendingByCategory(unittest.TestCase):  # type: ignore

    def setUp(self):  # type: ignore
        # Создаем тестовые данные
        self.test_data = pd.DataFrame(
            {
                "Дата операции": ["01.01.2023", "15.01.2023", "20.02.2023"],
                "Категория": ["Еда", "Еда", "Транспорт"],
                "Сумма операции": [-1000, -500, -300],
                "Сумма платежа": [1000, 500, 300],
            }
        )

    def test_spending_by_category_food(self):  # type: ignore
        result = spending_by_category(self.test_data, "еда", "15.04.2023")
        expected_total = 500
        self.assertEqual(result.iloc[0, 0], expected_total)
