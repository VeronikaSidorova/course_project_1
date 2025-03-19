from src.reports import spending_by_category
from src.services import search_transactions
from src.utils import reader_excel
from src.views import home_page


def main():  # type: ignore
    print("Введите дату для поиска ")
    date_input_ex = input()
    print(home_page(date_input_ex))
    print("Сервис простой поиск: введите запрос для поиска ")
    search_input = input()
    print(search_transactions(search_input))
    print("По какой категории хотите просмотреть траты за последние три месяца")
    category_search = input()
    return spending_by_category(reader_excel(), category_search)


if __name__ == "__main__":
    print(main())
