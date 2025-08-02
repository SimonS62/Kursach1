import os.path
import pandas as pd
import json
from datetime import datetime
from config import ROOT_DIR,API_KEY
from src.utils import fetch_top_transactions,get_stocks,get_greeting,get_total_expenses,get_last4,get_cashback,get_currency_rate


# Основная функция
def main_function(date_str):
    operations_path = os.path.join(ROOT_DIR, 'data', 'operations.xlsx')
    user_settings_path = os.path.join(ROOT_DIR, 'user_settings.json')
    try:
        data = pd.read_excel(operations_path, parse_dates=['Дата операции'])
    except Exception as e:
        return json.dumps({"error": f"Ошибка при чтении файла: {e}"})

    # Парсим дату
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return json.dumps({"error": "Некорректный формат даты"})

    start_dt = dt.replace(day=1, hour=0, minute=0, second=0)

    # Получаем приветствие
    greeting = get_greeting(datetime.now())
    print(greeting)

    # Чтение настроек пользователя
    try:
        with open(user_settings_path, 'r',
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
            'card_number': row.get('Номер карты', ''),
            'amount': row.get('Сумма операции', 0),
            'date': row.get('Дата операции')

        }
        transactions.append(transaction)

    # Фильтрация транзакций по дате (если нужно)
    filtered_transactions = [
        t for t in transactions
        if start_dt <= t['date'] <= dt
    ]

    total_expenses = get_total_expenses(filtered_transactions)

    # Формируем список карт с последними 4 цифрами и кешбэком
    cards_info = []
    for t in filtered_transactions:
        last4 = get_last4(str(t['card_number']))
        cashback = get_cashback(t['amount'])
        cards_info.append({
            'last4_digits': last4,
            'total_expenses': t['amount'],
            'cashback': cashback
        })

    # # Топ-5 транзакций по сумме
    # top_transactions = get_top_transactions(filtered_transactions)
    top_transactions = fetch_top_transactions(data)

    # Формируем ответ
    response = {
        "greeting": greeting,
        "cards": cards_info,
        "total_expenses": total_expenses,
        "currency_rates": get_currency_rate(user_currencies),
        "get_stocks": get_stocks(user_stocks),
        "top_transactions": top_transactions
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


# Пример вызова функции
if __name__ == "__main__":
    date_input = "2021-12-17 01:02:03"



