import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pandas import DataFrame
from config import API_KEY
from typing import Dict


load_dotenv()

api_key = os.getenv('API_KEY')  # Получаем API-ключ из переменной окружения

# Приветствие
def get_greeting(current_time):
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


# Функция подсчета общего расхода
def get_total_expenses(transactions):
    total = sum(
        t['Сумма операции'] for t in transactions
        if 'Сумма операции' in t and isinstance(t['Сумма операции'], (int, float)) and t['Сумма операции'] < 0
    )
    return total


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


# Функция получения курса валют
def get_currency_rate(currencys, amount=1) -> Dict[str, float]:
    rates = []
    for currency in currencys:
        api_url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": f"{API_KEY}"}
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            rate = data.get('result', {})
            rates.append({
              "currency": currency,
              "rate": rate
            })
        except Exception as e:
            import logging
            logging.error(f"Ошибка получения курсов валют: {e}")
            return {'USD': None, 'EUR': None}
    return rates


# Функция получения стоимости акций с API (Alpha Vantage)
def get_stocks(symbols):
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    url = f"https://www.alphavantage.co/query"
    stocks = []
    for symbol in symbols:
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
                stocks.append({
                  "stock": symbol,
                  "price": price_str
                })
            else:
                raise ValueError("Нет данных по цене")
        except Exception as e:
            print(f"Ошибка получения данных по {symbol}: {e}")


    return stocks



