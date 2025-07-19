import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')  # Получаем API-ключ из переменной окружения
    url = f"https://apilayer.com/marketplace/exchangerates_data-api/convert?to=RUB&from={currency}&amount={amount}"

    headers = {
        "apikey": api_key
    }


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


def get_last4(card_number):
    return card_number[-4:]


def get_total_expenses(transactions):
    total = sum(t['amount'] for t in transactions if t['amount'] < 0)
    return abs(total)


def get_cashback(total_expenses):
    cashback = total_expenses // 100
    return cashback


def fetch_top_transactions():
    transactions = [
        {'description': 'Покупка A', 'amount': 5000},
        {'description': 'Покупка B', 'amount': 3000},
        {'description': 'Покупка C', 'amount': 2000},
        {'description': 'Покупка D', 'amount': 1500},
        {'description': 'Покупка E', 'amount': 1200},
        {'description': 'Покупка F', 'amount': 800},
    ]
    top5 = sorted(transactions, key=lambda x: x['amount'], reverse=True)[:5]
    return top5


def fetch_currency_rates():
    eaders = {
        "apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        if 'result' in data:
            return float(data['result'])  # Возвращаем сумму в рублях
        else:
            print("Ошибка: Не удалось получить результат конвертации.")
            return None
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
        # Вернем курсы к USD
        return data['quotes']
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
        # Фиктивные данные при ошибке
        return {
            "USDEUR": 0.88,
            "USDGBP": 0.75,
            "USDJPY": 110.0,
            "USDCNY": 6.45
        }


def fetch_sp500_stocks():
    api_key = os.getenv('API_KEY')  # Получаем API-ключ из переменной окружения
    url = f"https://apilayer.com/marketplace/exchangerates_data-api/convert?to=RUB&from={currency}&amount={amount}

    def get_stock_price(symbol):
        url = f"https://apilayer.com/marketplace/exchangerates_data-api/convert?to=RUB&from={currency}&amount={amount}
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            price_str = data["Global Quote"].get("05. price")
            if price_str:
                return float(price_str)
            else:
                raise ValueError("Нет данных по цене")
        except Exception as e:
            print(f"Ошибка получения данных по {symbol}: {e}")
            # Фиктивные данные при ошибке
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



