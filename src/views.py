import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any


# Приветствие
def get_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_total_expenses(transactions: List[Dict[str, Any]]) -> float:
    # транзакции — список словарей с ключом 'amount'
    return sum(t['amount'] for t in transactions)


def get_last4_digits(card_number: str) -> str:
    return card_number[-4:] if len(card_number) >= 4 else card_number


def get_cashback(amount: float) -> float:
    # логика кешбэка
    return abs(amount) * 0.01


def get_currency_rate() -> Dict[str, float]:
    # Заглушка для получения курсов валют
    return {"USD": 1.0, "EUR": 0.85}


def get_sp500_price() -> float:
    # Заглушка для стоимости индекса S&P 500
    return 4200.0


def get_top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Топ-5 транзакций по сумме
    sorted_tx = sorted(transactions, key=lambda x: abs(x['amount']), reverse=True)
    return sorted_tx[:5]


# Основная функция
def main_function(date_str):
    try:
        data = pd.read_excel('../data/operations.xlsx', parse_dates=['Дата операции'])
    except Exception as e:
        return json.dumps({"error": f"Ошибка при чтении файла: {e}"})

    # Парсим дату
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return json.dumps({"error": "Некорректный формат даты"})

    start_dt = dt.replace(day=1, hour=0, minute=0, second=0)

    # Получаем приветствие
    greeting = get_greeting(datetime.now().hour)

    # Чтение настроек пользователя
    try:
        with open(r'..\Users\Windows\PycharmProjects\ProjectKursach1\user_settings.json', 'r',
                  encoding='utf-8') as file:
            user_settings = json.load(file)
    except Exception as e:
        return json.dumps({"error": f"Ошибка при чтении настроек: {e}"})

    user_currencies = user_settings.get('user_currencies', [])
    user_stocks = user_settings.get('user_stocks', [])

    # Выводим списки
    print("Валюты пользователя:", user_currencies)
    print("Акции пользователя:", user_stocks)

    # Обработка транзакций - предполагается, что данные из файла или другого источника
    transactions = []

    # колонка 'Категория' и 'Сумма операции'
    for _, row in data.iterrows():
        transaction = {
            'card_number': row.get('Карта', ''),
            'amount': row.get('Сумма операции', 0),
            'Дата': row.get('Дата операции')

        }
        transactions.append(transaction)

    # Фильтрация транзакций по дате (если нужно)
    filtered_transactions = [
        t for t in transactions
        if start_dt <= t['Дата'] <= dt
    ]

    total_expenses = get_total_expenses(filtered_transactions)

    # Формируем список карт с последними 4 цифрами и кешбэком
    cards_info = []
    for t in filtered_transactions:
        last4 = get_last4_digits(t['card_number'])
        cashback = get_cashback(t['amount'])
        cards_info.append({
            'last4_digits': last4,
            'total_expenses': t['amount'],
            'cashback': cashback
        })

    # Топ-5 транзакций по сумме
    top_transactions = get_top_transactions(filtered_transactions)

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


