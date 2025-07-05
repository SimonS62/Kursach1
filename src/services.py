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
        lambda t: t['date'].year == year and t['date'].month == month,
        data
    ))

    # Для каждой категории считаем сумму расходов
    def reducer(acc, t):
        category = t['category']
        amount = t['expenses']
        acc[category] = acc.get(category, 0) + amount
        return acc

    category_sums = reduce(reducer, filtered, {})

    # Вычисляем кешбэк по каждой категории
    cashback_per_category = {
        cat: round(amount * CASHBACK_RATES.get(cat, 0))
        for cat, amount in category_sums.items()
    }

    return json.dumps(cashback_per_category, ensure_ascii=False, indent=2)


def invest_savings(data, rounding_threshold=50):
    """
    Округляет траты и копит разницу на счет «Инвесткопилка».

    :param data: список транзакций (dict), каждая с датой и расходами.
    :param rounding_threshold: порог округления (10/50/100).
    :return: JSON с итогами по округлению и накопленным средствам.
    """

    def round_amount(amount):
        """Округляет сумму до ближайшего кратного порогу."""
        return ((amount + rounding_threshold - 1) // rounding_threshold) * rounding_threshold

    total_spent = sum(t['expenses'] for t in data)

    # Для каждой транзакции считаем округленную сумму и разницу
    def process_transaction(t):
        original = t['expenses']
        rounded = round_amount(original)
        difference = rounded - original
        return {
            'original': original,
            'rounded': rounded,
            'difference': difference
        }

    processed = list(map(process_transaction, data))

    total_rounded = sum(t['rounded'] for t in processed)
    total_difference = sum(t['difference'] for t in processed)

    result = {
        'Общие траты': total_spent,
        'Общая сумма после округления': total_rounded,
        'Накопленная сумма на инвесткопилке': total_difference
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


# Пример использования внутри модуля или тестов:
if __name__ == "__main__":
    # Пример данных
    transactions = [
        {'date': datetime(2024, 4, 10), 'category': 'Продукты', 'expenses': 123},
        {'date': datetime(2024, 4, 15), 'category': 'Транспорт', 'expenses': 47},
        {'date': datetime(2024, 4, 20), 'category': 'Развлечения', 'expenses': 200},
        {'date': datetime(2024, 4, 25), 'category': 'Подарки', 'expenses': 550},
        {'date': datetime(2024, 3, 30), 'category': 'Продукты', 'expenses': 300}
    ]

    print("Анализ кешбэка за апрель 2024:")
    print(analyze_cashback_categories(transactions, [2024], [4]))

    print("\nИнвесткопилка при пороге округления 50:")
    print(invest_savings(transactions, [2024], [4], rounding_threshold=50))

