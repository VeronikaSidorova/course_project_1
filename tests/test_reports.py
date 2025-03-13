import pandas as pd
import pytest

from src.reports import spending_by_category
from src.utils import transactions


@pytest.fixture
def get_operations_df():  # type: ignore
    transactions_df = pd.DataFrame(transactions)
    return transactions_df


def test_spending_by_category(get_operations_df):  # type: ignore
    actual = spending_by_category(get_operations_df, "Аптеки", "06.01.2020")
    expected = -2737.0
    assert actual == expected
