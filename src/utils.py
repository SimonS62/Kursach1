import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()

api_key = os.getenv('API_KEY')  # Получаем API-ключ из переменной окружения


def get_greeting(current_time_str):
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S").time()
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# Функция получения последних 4 цифр карты
def get_last4(card_number):
    return card_number[-4:] if len(card_number) >= 4 else card_number


# Функция подсчета общего расхода (сумма отрицательных транзакций)
def get_total_expenses(transactions):
    total = sum(t['Сумма операции'] for t in transactions if t['Сумма операции'] < 0)
    return abs(total)


# Функция расчета кешбэка (например, 1% от расходов)
def get_cashback(total_expenses):
    cashback = total_expenses * 0.01
    return cashback


# Функция получения топ-5 транзакций по сумме
def fetch_top_transactions(sorted_df:DataFrame):
    top_pay_transactions = []
    top5 = sorted_df.sort_values(by='Сумма операции',ascending=False)
    top_transactions = top5.head(5)
    top_transactions_sorted = top_transactions[
        ['Дата операции', 'Сумма операции', 'Категория', 'Описание']
    ]
    for i,v in top_transactions_sorted.iterrows():
        v = {
            "date": f'{v["Дата операции"]}',
            "amount": f'{v["Сумма операции"]}',
            "category": f'{v["Категория"]}',
            "description": f'{v["Описание"]}'
        }
        top_pay_transactions.append(v)
    return top_pay_transactions


# # Функция получения курса валют с API
# api_key = os.getenv('API_KEY')  # Получаем API-ключ из переменной окружения
#     url = f"https://apilayer.com/marketplace/exchangerates_data-api/convert?to=RUB&from={currency}&amount={amount}"
#
#     headers = {
#         "apikey": api_key
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         return data.get('rates', {})  # возвращает словарь курсов валют
#     except requests.RequestException as e:
#         print(f"Ошибка при запросе к API: {e}")


# Функция получения стоимости акций с API (например, Alpha Vantage)
def fetch_sp500_stocks():
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

    def get_stock_price(symbol):
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            price_str = data.get("Global Quote", {}).get("05. price")
            if price_str:
                return float(price_str)
            else:
                raise ValueError("Нет данных по цене")
        except Exception as e:
            print(f"Ошибка получения данных по {symbol}: {e}")
            # Возвращаем фиктивные данные при ошибке
            return {
                "AAPL": 170,
                "MSFT": 290,
                "GOOGL": 2800
            }.get(symbol, None)

    stocks_symbols = ["AAPL", "MSFT", "GOOGL"]
    stocks_info = []
    for symbol in stocks_symbols:
        price = get_stock_price(symbol)
        stocks_info.append({
            "ticker": symbol,
            "price": price
        })

    return stocks_info



