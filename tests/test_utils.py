import unittest
import pandas as pd
from unittest.mock import patch, Mock
from datetime import datetime
from src.utils import get_total_expenses,fetch_top_transactions,get_greeting,get_last4,get_cashback,get_currency_rate,get_stocks

class TestFinanceFunctions(unittest.TestCase):

    def test_get_total_expenses(self):
        transactions = [
            {'Сумма операции': -100},
            {'Сумма операции': -200},
            {'Сумма операции': 50},  # доход, не учитываем
            {'Сумма операции': -50}
        ]
        total = get_total_expenses(transactions)
        self.assertEqual(total, -350)

    def test_fetch_top_transactions(self):
        data = {
            'Дата операции': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05', '2023-10-06'],
            'Сумма операции': [300, 500, 200, 700, 400, 600],
            'Категория': ['Категория1']*6,
            'Описание': ['Описание1']*6
        }
        df = pd.DataFrame(data)
        top_transactions = fetch_top_transactions(df)
        self.assertEqual(len(top_transactions), 5)
        # Проверяем, что самый большой транзакции — это 700
        self.assertEqual(float(top_transactions[0]['amount']), 700)

    def test_get_greeting_morning(self):
        time_obj = datetime(2023, 10, 1, 6)
        self.assertEqual(get_greeting(time_obj), "Доброе утро")

    def test_get_greeting_day(self):
        time_obj = datetime(2023, 10, 1, 13)
        self.assertEqual(get_greeting(time_obj), "Добрый день")

    def test_get_last4(self):
        self.assertEqual(get_last4("1234567890123456"), "3456")
        self.assertEqual(get_last4("123"), "123")

    def test_get_cashback(self):
        total = -200
        cashback = get_cashback(total)
        self.assertAlmostEqual(cashback, -2.0)

    @unittest.mock.patch('src.utils.requests.get')
    def test_get_currency_rate(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'result': 75.5}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        rates = get_currency_rate(['USD', 'EUR'])
        self.assertIsInstance(rates, list)
        for rate in rates:
            self.assertIn('currency', rate)
            self.assertIn('rate', rate)
            self.assertEqual(rate['rate'], 75.5)

    @unittest.mock.patch('src.utils.requests.get')
    def test_get_stocks(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            "Global Quote": {
                "05. price": "150.25"
            }
        }
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        stocks = get_stocks(['AAPL'])
        self.assertEqual(len(stocks), 1)
        self.assertEqual(stocks[0]['stock'], 'AAPL')
        self.assertEqual(stocks[0]['price'], "150.25")


if __name__ == '__main__':
    unittest.main()