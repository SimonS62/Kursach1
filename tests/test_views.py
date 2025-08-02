import unittest
from unittest.mock import patch
import json
from datetime import datetime
from src.views import main_function


class TestMainFunction(unittest.TestCase):
    @patch('pandas.read_excel')
    @patch('src.utils.open')
    @patch('src.utils.get_greeting')
    @patch('src.utils.get_total_expenses')
    @patch('src.utils.fetch_top_transactions')
    @patch('src.utils.get_currency_rate')
    @patch('src.utils.get_stocks')
    def test_main_function_success(self,
                                   mock_get_stocks,
                                   mock_get_currency_rate,
                                   mock_fetch_top_transactions,
                                   mock_get_total_expenses,
                                   mock_get_greeting,
                                   mock_open,
                                   mock_read_excel):

        # Настраиваем мок pandas DataFrame
        import pandas as pd
        df_mock = pd.DataFrame({
            'Номер карты': ['1234567812345678'],
            'Сумма операции': [200],
            'Дата операции': [pd.Timestamp('2021-12-17 00:00:00')],
            'Категория': ['Покупка'],
            'Описание': ['Описание 1']
        })
        mock_read_excel.return_value = df_mock

        # Мокаем get_greeting
        mock_get_greeting.return_value = "Добрый день"

        # Мокаем get_total_expenses
        mock_get_total_expenses.return_value = 200

        # Мокаем fetch_top_transactions
        mock_fetch_top_transactions.return_value = [{"transaction": "top1"}]

        # Мокаем get_currency_rate
        mock_get_currency_rate.return_value = {"USD": 1.0}

        # Мокаем get_stocks
        mock_get_stocks.return_value = ["AAPL", "GOOG"]

        # Мокаем open для настроек
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
            'user_currencies': ['USD', 'EUR'],
            'user_stocks': ['AAPL', 'TSLA']
        })

        # Вызов функции с тестовой датой
        test_date_str = '2021-12-17 00:00:00'
        result_json = main_function(test_date_str)

        # Проверка результата (парсим JSON)
        result = json.loads(result_json)

        self.assertEqual(result['greeting'], "Добрый день")
        self.assertIn('cards', result)
        self.assertEqual(result['total_expenses'], 0)
        self.assertIn('currency_rates', result)
        self.assertIn('get_stocks', result)
        self.assertIn('top_transactions', result)


if __name__ == '__main__':
    unittest.main()