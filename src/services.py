import json
from datetime import datetime
from functools import reduce
import logging
from collections import defaultdict

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
        amount = t['Кэшбэк'] if float(t['Кэшбэк']) > 0 else 0
        if amount:
            acc[category] += amount
        return acc

    category_sums = reduce(reducer, filtered, defaultdict(int))


    return json.dumps(cashback_per_category, ensure_ascii=False, indent=2)


# Пример использования внутри модуля или тестов:
if __name__ == "__main__":
    # Пример данных
    data = pd.read_excel('../data/operations.xlsx', parse_dates=['Дата операции']).to_dict('records')

    print("Анализ кешбэка за ноябрь 2021:")
    print(analyze_cashback_categories(data, 2021, 11))


