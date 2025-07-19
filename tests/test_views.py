import unittest
from unittest.mock import patch, MagicMock
import json

# Предположим, что main_function находится в модуле src.views
from src.views import main_function

class TestMainFunction(unittest.TestCase):
    @patch('src.views.get_greeting')
    @patch('src.views.get_total_expenses')
    @patch('src.views.get_last4_digits')
    @patch('src.views.get_cashback')
    @patch('src.views.get_top_transactions')
    @patch('src.views.get_currency_rate')
    @patch('src.views.get_sp500_price')
    def test_main_function(self, mock_get_sp500_price, mock_get_currency_rate,
                           mock_get_top_transactions, mock_get_cashback,
                           mock_get_last4_digits, mock_get_total_expenses,
                           mock_get_greeting):
        # Настраиваем моки
        mock_get_greeting.return_value = "Добрый день!"
        mock_get_total_expenses.return_value = 1500
        mock_get_last4_digits.side_effect = ['1234', '5678']
        mock_get_cashback.side_effect = [10, 20]
        mock_get_top_transactions.return_value = [
            {"id": 1, "amount": 500},
            {"id": 2, "amount": 300}
        ]
        mock_get_currency_rate.return_value = {"USD": 1.0}
        mock_get_sp500_price.return_value = 4200.50

        # Вызов функции с тестовой датой
        test_date = "2024-04-27 15:30:00"
        result_json = main_function(test_date)
        result = json.loads(result_json)

        # Проверки
        self.assertEqual(result["greeting"], "Добрый день!")
        self.assertEqual(result["total_expenses"], 1500)
        self.assertEqual(len(result["cards"]), 2)
        self.assertEqual(result["cards"][0]["last4_digits"], "1234")
        self.assertEqual(result["cards"][1]["last4_digits"], "5678")
        self.assertEqual(result["cards"][0]["cashback"], 10)
        self.assertEqual(result["cards"][1]["cashback"], 20)
        self.assertEqual(result["currency_rates"], {"USD": 1.0})
        self.assertEqual(result["sp500_price"], 4200.50)
        self.assertEqual(len(result["top_transactions"]), 2)

if __name__ == '__main__':
    unittest.main()
