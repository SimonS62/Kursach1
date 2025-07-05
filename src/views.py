import json
from datetime import datetime


def main_function(date_str):
    # Парсим дату
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return json.dumps({"error": "Некорректный формат даты"})

    # Получаем приветствие
    greeting = get_greeting(dt.hour)

    # Пример данных о транзакциях (заглушки)
    transactions = [
        {'card_number': '1234567812345678', 'amount': 1500},
        {'card_number': '8765432187654321', 'amount': 2500},
        {'card_number': '1111222233334444', 'amount': 500},
        {'card_number': '5555666677778888', 'amount': 3000},
        {'card_number': '9999000011112222', 'amount': 200},
        {'card_number': '3333444455556666', 'amount': 3500},
    ]

    # Обработка транзакций
    total_expenses = get_total_expenses(transactions)

    # Формируем список карт с последними 4 цифрами и кешбэком
    cards_info = []
    for t in transactions:
        last4 = get_last4_digits(t['card_number'])
        cashback = get_cashback(t['amount'])
        cards_info.append({
            'last4_digits': last4,
            'total_expenses': t['amount'],
            'cashback': cashback
        })

    # Топ-5 транзакций по сумме
    top_transactions = get_top_transactions(transactions)

    # Формируем ответ
    response = {
        "greeting": greeting,
        "cards": cards_info,
        "total_expenses": total_expenses,
        "currency_rates": get_currency_rate(),
        "sp500_price": get_sp500_price(),
        "top_transactions": top_transactions
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


# Пример вызова функции
if __name__ == "__main__":
    date_input = "2024-04-27 15:30:00"
    print(main_function(date_input))


def process_date(date_str):
    """
    Принимает строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
    и возвращает объект datetime или выполняет нужные операции.
    """
    try:
        # Преобразуем строку в объект datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        # Можно выполнить дополнительные операции с датой
        return date_obj
    except ValueError:
        print("Некорректный формат даты. Используйте 'YYYY-MM-DD HH:MM:SS'.")
        return None


def main_function(date_str, range_type='M'):
    # Получаем диапазон дат
    start_dt, end_dt = get_date_range(date_str, range_type)

    # Заготовка транзакций (примерные данные)
    transactions_data = [
        {'date': datetime(2024, 4, 1), 'category': 'Продукты', 'expenses': 1500, 'income': 0},
        {'date': datetime(2024, 4, 3), 'category': 'Транспорт', 'expenses': 300, 'income': 0},
        {'date': datetime(2024, 4, 5), 'category': 'Зарплата', 'expenses': 0, 'income': 30000},
        {'date': datetime(2024, 4, 10), 'category': 'Развлечения', 'expenses': 2000, 'income': 0},
        {'date': datetime(2024, 4, 15), 'category': 'Подарки', 'expenses': 5000, 'income': 0},
        {'date': datetime(2024, 4, 20), 'category': 'Переводы', 'expenses': 0, 'income': 10000},
        {'date': datetime(2024, 4, 25), 'category': "Наличные", "expenses": 2500, "income": 0},
        {'date': datetime(2024, 4, 27), 'category': 'Продукты', 'expenses': 1200, 'income': 0},
        {'date': datetime(2024, 3, 28), 'category': 'Зарплата', 'expenses': 0, 'income': 25000}
    ]

    # Фильтруем транзакции по диапазону дат
    filtered_tx = filter_transactions(transactions_data, start_dt, end_dt)

    # Расходы и поступления за выбранный период
    total_expenses, _ = get_expenses_and_income(filtered_tx)

    total_income = sum(t['income'] for t in filtered_tx)

    # Категории расходов (топ-7 + "Остальное")
    expenses_by_category = get_top_categories(filtered_tx, 'expenses', 7)

    # Категории переводов и наличных (по сумме расходов/доходов)
    cash_withdrawals = sum(t['expenses'] for t in filtered_tx if t['category'] == "Наличные")
    transfers = sum(t['income'] for t in filtered_tx if t['category'] == "Переводы")

    cash_transfers = [
        {'category': 'Наличные', 'amount': round(cash_withdrawals)},
        {'category': 'Переводы', 'amount': round(transfers)}
    ]

    # Поступления по категориям (топ-7 + "Остальное")
    income_by_category = get_top_categories(filtered_tx, 'income', 7)

    # Формируем ответ
    response = {
        "Расходы": {
            "Общая сумма": round(total_expenses),
            "Основные": expenses_by_category,
            "Переводы и наличные": cash_transfers
        },
        "Поступления": {
            "Общая сумма": round(total_income),
            "Основные": income_by_category
        },
        "Курс валют": get_currency_rate(),
        "Стоимость акций S&P500": get_sp500_price()
    }

    return json.dumps(response, note_ascii=False, ensure_ascii=False, indent=2)


# Пример вызова функции:
if __name__ == "__main__":
    print(main_function("2024-04-27 15:30:00", range_type='M')





