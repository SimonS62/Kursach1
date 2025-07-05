import json
from datetime import datetime


def get_greeting(hour):
    """Возвращает приветствие в зависимости от часа."""
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_last4_digits(card_number):
    """Возвращает последние 4 цифры номера карты."""
    return card_number[-4:]


def get_total_expenses(transactions):
    """Подсчитывает общую сумму расходов из списка транзакций."""
    return sum(t['amount'] for t in transactions)


def get_cashback(amount):
    """Вычисляет кешбэк (1 рубль на каждые 100 рублей)."""
    return amount // 100


def get_top_transactions(transactions, top_n=5):
    """Возвращает топ-N транзакций по сумме."""
    sorted_tx = sorted(transactions, key=lambda t: t['amount'], reverse=True)
    return sorted_tx[:top_n]


def get_currency_rate():
    """Возвращает курс валют. Заглушка."""
    return {
        'USD': 75.0,
        'EUR': 88.0,
        'RUB': 1.0
    }


def get_sp500_price():
    """Стоимость акций S&P500. Заглушка."""
    return 4200.50


def get_date_range(date_str, range_type='M'):
    """
    Возвращает начало и конец диапазона дат в формате datetime.
    range_type: 'W', 'M', 'Y', 'ALL'
    """
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    if range_type == 'ALL':
        # Возвращаем очень раннюю дату и саму дату
        start_date = datetime(2000, 1, 1)
        end_date = date
    elif range_type == 'W':
        # Неделя: последние 7 дней до даты включительно
        start_date = date - timedelta(days=6)
        end_date = date
    elif range_type == 'M':
        # Месяц: с первого числа месяца по дату
        start_date = date.replace(day=1)
        end_date = date
    elif range_type == 'Y':
        # Год: с 1 января по дату
        start_date = date.replace(month=1, day=1)
        end_date = date
    else:
        # По умолчанию — месяц
        start_date = date.replace(day=1)
        end_date = date

    return start_date, end_date


def filter_transactions(transactions, start_date, end_date):
    """Фильтрует транзакции по дате."""
    return [t for t in transactions if start_date <= t['date'] <= end_date]


def get_top_categories(transactions, key='expenses', top_n=7):
    """
    Возвращает топ N категорий по сумме.
    key: 'expenses' или 'income'
    """
    category_sums = defaultdict(float)
    for t in transactions:
        category_sums[t['category']] += t[key]

    sorted_cats = sorted(category_sums.items(), key=lambda x: x[1], reverse=True)

    top_categories = sorted_cats[:top_n]

    # Остальные категории суммируем в "Остальное"
    other_sum = sum(amount for _, amount in sorted_cats[top_n:])

    result = []
    for cat, amount in top_categories:
        result.append({'category': cat, 'amount': round(amount)})

    if other_sum > 0:
        result.append({'category': 'Остальное', 'amount': round(other_sum)})

    return result


def get_expenses_and_income(transactions):
    """Подсчитывает общие расходы и поступления."""
    total_expenses = sum(t['expenses'] for t in transactions)
    total_income = sum(t['income'] for t in transactions)

    return round(total_expenses), round(total_income)


def get_currency_rate():
    """Заглушка для курса валют."""
    return {
        'USD': 75.0,
        'EUR': 88.0,
        'RUB': 1.0
    }


def get_sp500_price():
    """Заглушка для стоимости S&P500."""
    return 4200.50




