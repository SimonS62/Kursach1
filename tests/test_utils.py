import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os


class TestFunctions(unittest.TestCase):

    def test_get_greeting_morning(self):
        self.assertEqual(get_greeting("2024-04-27 06:30:00"), "Доброе утро")

    def test_get_greeting_day(self):
        self.assertEqual(get_greeting("2024-04-27 13:00:00"), "Добрый день")

    def test_get_greeting_evening(self):
        self.assertEqual(get_greeting("2024-04-27 18:30:00"), "Добрый вечер")

    def test_get_greeting_night(self):
        self.assertEqual(get_greeting("2024-04-27 02:00:00"), "Доброй ночи")

    def test_get_last4(self):
        self.assertEqual(get_last4("1234567890123456"), "3456")
        self.assertEqual(get_last4("9876543210"), "3210")

    def test_get_total_expenses(self):
        transactions = [
            {'amount': -100},
            {'amount': -200},
            {'amount': 50},
            {'amount': -300}
        ]
        self.assertEqual(get_total_expenses(transactions), 600)

    def test_get_cashback(self):
        self.assertEqual(get_cashback(250), 2)
        self.assertEqual(get_cashback(99), 0)
        self.assertEqual(get_cashback(1000), 10)

    @patch('requests.get')
    def test_fetch_currency_rates_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': '75.5'}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = fetch_currency_rates()
        self.assertEqual(result, 75.5)

    @patch('requests.get')
    def test_fetch_currency_rates_failure(self, mock_get):
        # Симуляция исключения
        mock_get.side_effect = Exception("Ошибка сети")
        result = fetch_currency_rates()
        # Ожидается словарь с курсами по умолчанию
        self.assertIn('USDEUR', result)

    @patch('requests.get')
    def test_fetch_sp500_stocks_success(self, mock_get):
        # Мокаем ответ API для каждого символа
        def side_effect(url, params=None):
            symbol = params['symbol']
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "Global Quote": {
                    "05. price": str(150 + hash(symbol) % 50)
                }
            }
            mock_resp.raise_for_status = lambda: None
            return mock_resp

        mock_get.side_effect = side_effect

        stocks_info = fetch_sp500_stocks()
        self.assertIsInstance(stocks_info, list)
        for stock in stocks_info:
            self.assertIn('ticker', stock)
            self.assertIn('price', stock)
            self.assertIsInstance(stock['price'], float)

    @patch('requests.get')
    def test_fetch_sp500_stocks_error(self, mock_get):
        # Симуляция ошибки при запросе
        mock_get.side_effect = Exception("API недоступен")

        stocks_info = fetch_sp500_stocks()
        # Должен вернуть список с дефолтными значениями
        for stock in stocks_info:
            self.assertIn('ticker', stock)
            self.assertIn('price', stock)


if __name__ == '__main__':
    unittest.main()

