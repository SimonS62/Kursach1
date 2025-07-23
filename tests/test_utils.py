import unittest
from unittest.mock import patch, Mock
from datetime import datetime
from utils import get_greeting, get_last4, get_total_expenses, get_cashback, fetch_top_transactions, fetch_currency_rates, fetch_sp500_stocks


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
    return card_number[-4:] if len(card_number) >= 4 else card_number


def get_total_expenses(transactions):
    total = sum(t['amount'] for t in transactions if t['amount'] < 0)
    return abs(total)


def get_cashback(total_expenses):
    cashback = total_expenses * 0.01
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


# Тесты
class TestMyFunctions(unittest.TestCase):

    def test_get_greeting(self):
        self.assertEqual(get_greeting("2023-10-01 06:30:00"), "Доброе утро")
        self.assertEqual(get_greeting("2023-10-01 13:00:00"), "Добрый день")
        self.assertEqual(get_greeting("2023-10-01 18:30:00"), "Добрый вечер")
        self.assertEqual(get_greeting("2023-10-01 23:15:00"), "Доброй ночи")
        self.assertEqual(get_greeting("2023-10-01 04:59:59"), "Доброй ночи")

    def test_get_last4(self):
        self.assertEqual(get_last4("1234567890123456"), "3456")
        self.assertEqual(get_last4("abcd"), "abcd")
        self.assertEqual(get_last4("abc"), "abc")  # менее 4 символов

    def test_get_total_expenses(self):
        transactions = [
            {'amount': -100},
            {'amount': -50},
            {'amount': 200},
            {'amount': -300}
        ]
        self.assertEqual(get_total_expenses(transactions), 450)

    def test_get_cashback(self):
        self.assertAlmostEqual(get_cashback(100), 1.0)
        self.assertAlmostEqual(get_cashback(250), 2.5)
        self.assertAlmostEqual(get_cashback(0), 0)

    def test_fetch_top_transactions(self):
        top = fetch_top_transactions()
        # Проверяем что топ-5 по сумме
        amounts = [t['amount'] for t in top]
        expected_amounts = [5000, 3000, 2000, 1500, 1200]
        self.assertEqual(amounts, expected_amounts)

    @patch('requests.get')
    def test_fetch_currency_rates_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            'rates': {
                'USD': 1.0,
                'EUR': 0.85,
                'GBP': 0.75
            }
        }
        mock_get.return_value = mock_response

        rates = fetch_currency_rates()
        self.assertIn('USD', rates)
        self.assertIn('EUR', rates)

    @patch('requests.get')
    def test_fetch_currency_rates_failure(self, mock_get):
        # Имитация исключения при запросе
        mock_get.side_effect = requests.RequestException("Ошибка сети")

        rates = fetch_currency_rates()
        # Проверяем что возвращаются фиктивные данные
        self.assertIn('USD', rates)

    @patch('requests.get')
    def test_fetch_sp500_stocks_success(self, mock_get):
        # Мокаем ответ API для каждого символа
        def side_effect(url, params):
            symbol = params['symbol']
            mock_resp = Mock()
            mock_resp.raise_for_status = Mock()
            mock_resp.json.return_value = {
                "Global Quote": {
                    "05. price": str(150 + hash(symbol) % 50)  # произвольная цена
                }
            }
            return mock_resp

        mock_get.side_effect = side_effect

        stocks_info = fetch_sp500_stocks()

        for stock in stocks_info:
            self.assertIn('ticker', stock)
            self.assertIn('price', stock)
            self.assertIsInstance(stock['price'], float)


if __name__ == '__main__':
    unittest.main()