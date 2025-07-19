import json
from datetime import datetime
from utils import get_greeting


def main_function(date_str):
    # Парсим дату
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return json.dumps({"error": "Некорректный формат даты"})
    start_dt = dt.replace(day=1, hour=0, minute=0, second=0)
    # Получаем приветствие
    greeting = get_greeting(datetime.now().hour)

    with open(r'C:\Users\Windows\PycharmProjects\ProjectKursach1\user_settings.json', 'r', encoding='utf-8') as file:
        user_settings = json.load(file)

    # Получаем списки из файла
    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']

    # Проверка
    print("Валюты пользователя:", user_currencies)
    print("Акции пользователя:", user_stocks)
    # запросить курсы валют
    # запросить стоимость акций

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


