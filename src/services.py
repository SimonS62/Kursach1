import json
from datetime import datetime
from functools import reduce
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Константы для кешбэка (примерные ставки по категориям)
CASHBACK_RATES = {
    'Продукты': 0.05,
    'Транспорт': 0.02,
    'Развлечения': 0.03,
    'Подарки': 0.04,
    'Зарплата': 0.00,
    'Переводы': 0.00,
    'Наличные': 0.00,
}


def analyze_cashback_categories(data, year, month):
    """
    Анализирует, сколько можно заработать кешбэка по категориям за указанный месяц.

    :param data: список транзакций (dict), каждая с датой, категорией и расходами.
    :param year: год анализа.
    :param month: месяц анализа.
    :return: JSON строка с категориями и суммами кешбэка.
    """
    # Фильтруем транзакции по году и месяцу
    filtered = list(filter(
        lambda t: t['Дата операции'].year == year and t['Дата операции'].month == month,
        data
    ))

    # Для каждой категории считаем сумму расходов
    def reducer(acc, t):
        category = t['Категория']
        amount = t['Сумма операции']
        acc[category] = acc.get(category, 0) + amount
        return acc

    category_sums = reduce(reducer, filtered, {})

    # Вычисляем кешбэк по каждой категории
    cashback_per_category = {
        cat: round(amount * CASHBACK_RATES.get(cat, 0))
        for cat, amount in category_sums.items()
    }

    return json.dumps(cashback_per_category, ensure_ascii=False, indent=2)


# Пример использования внутри модуля или тестов:
if __name__ == "__main__":
    # Пример данных
    transactions = [
        {'Дата операции': datetime(2021, 11, 10), 'Категория': 'Продукты', 'expenses': 123},
        {'Дата операции': datetime(2021, 11, 15), 'Категория': 'Транспорт', 'expenses': 47},
        {'Дата операции': datetime(2021, 11, 20), 'Категория': 'Развлечения', 'expenses': 200},
        {'Дата операции': datetime(2021, 11, 25), 'Категория': 'Подарки', 'expenses': 550},
        {'Дата операции': datetime(2021, 11, 30), 'Категория': 'Продукты', 'expenses': 300}
    ]

    print("Анализ кешбэка за ноябрь 2021:")
    print(analyze_cashback_categories(transactions, [2021], [11]))


