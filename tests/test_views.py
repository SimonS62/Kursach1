import unittest
from unittest.mock import patch
import json
from datetime import datetime


class TestMainFunction(unittest.TestCase):

    @patch('ваш_модуль.get_greeting')
    @patch('ваш_модуль.get_total_expenses')
    @patch('ваш_модуль.get_last4_digits')
    @patch('ваш_модуль.get_cashback')
    @patch('ваш_модуль.get_top_transactions')
    @patch('ваш_модуль.get_currency_rate')
    @patch('ваш_модуль.get_sp500_price')
    @patch('ваш_модуль.datetime')
    def test_main_function_success(self, mock_datetime, mock_sp500, mock_currency_rate,
                                   mock_get_cashback,
                                   mock_get_last4_digits, mock_get_total_expenses,
                                   mock_get_greeting):
        # Настраиваем дату и время
        mock_datetime.now.return_value = datetime(2024, 4, 27, 14, 0)
        mock_datetime.strptime = datetime.strptime

        # Моки для внешних функций
        mock_get_greeting.return_value = "Добрый день"
        mock_get_total_expenses.return_value = 1500
        mock_get_last4_digits.side_effect = lambda card_number: card_number[-4:]
        mock_get_cashback.return_value = 5
        mock_get_top_transactions.return_value = [
            {"amount": 300, "category": "Food"},
            {"amount": 200, "category": "Transport"}
        ]
        mock_currency_rate.return_value = {"USD": 1.0}
        mock_sp500.return_value = 4200.5

        # Входные данные
        date_str = '2024-04-01 12:00:00'

        # Вызов функции
        result_json = main_function(date_str)
        result = json.loads(result_json)

        # Проверки
        self.assertIn("greeting", result)
        self.assertEqual(result["greeting"], "Добрый день")
        self.assertIn("cards", result)
        self.assertIn("total_expenses", result)
        self.assertEqual(result["total_expenses"], 1500)
        self.assertIn("currency_rates", result)
        self.assertIn("sp500_price", result)
        self.assertIn("top_transactions", result)

    def test_main_function_invalid_date(self):
        invalid_date_str = 'invalid-date'
        result_json = main_function(invalid_date_str)
        result = json.loads(result_json)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Некорректный формат даты")

if __name__ == '__main__':
    unittest.main()

class TestProcessDate(unittest.TestCase):

    def test_valid_date(self):
        # Тест с корректной датой
        date_str = '2024-04-27 15:30:45'
        result = process_date(date_str)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 4)
        self.assertEqual(result.day, 27)
        self.assertEqual(result.hour, 15)
        self.assertEqual(result.minute, 30)
        self.assertEqual(result.second, 45)

    def test_invalid_date_format(self):
        # Тест с некорректным форматом даты
        invalid_date_str = '27-04-2024 15:30:45'
        result = process_date(invalid_date_str)
        self.assertIsNone(result)

    def test_empty_string(self):
        # Тест с пустой строкой
        empty_str = ''
        result = process_date(empty_str)
        self.assertIsNone(result)

    def test_incorrect_format(self):
        # Тест с неправильным форматом
        wrong_format_str = '2024/04/27 15:30:45'
        result = process_date(wrong_format_str)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()


class TestMainFunction(unittest.TestCase):

    @patch('main_function.get_date_range')
    @patch('main_function.get_expenses_and_income')
    @patch('main_function.get_top_categories')
    @patch('main_function.get_currency_rate')
    @patch('main_function.get_sp500_price')
    def test_main_function(self, mock_get_sp500, mock_get_currency, mock_get_top_categories,
                                     mock_get_expenses_income, mock_get_date_range):
        # Настраиваем моки
        mock_get_date_range.return_value = (
            datetime(2024, 4, 1),
            datetime(2024, 4, 30)
        )

        # Возвращаемые значения для get_expenses_and_income
        mock_get_expenses_income.return_value = (total_expenses := 9500, total_income := 35000)

        # get_top_categories возвращает список топ-7 категорий
        mock_get_top_categories.side_effect = [
            [{'category': 'Продукты', 'amount': 2700}, {'category': 'Развлечения', 'amount': 2000}],
            [{'category': 'Зарплата', 'amount': 30000}]
        ]

        # Возвращаемые значения для get_currency_rate и get_sp500_price
        mock_get_currency.return_value = {'USD': 1.0}
        mock_get_sp500.return_value = 4200.5

        # Вызов функции
        result_json = main_function('2024-04-01 00:00:00')
        result = json.loads(result_json)

        # Проверки структуры результата
        self.assertIn("Расходы", result)
        self.assertIn("Общая сумма", result["Расходы"])
        self.assertEqual(result["Расходы"]["Общая сумма"], round(total_expenses))

        self.assertIn("Основные", result["Расходы"])
        self.assertIsInstance(result["Основные"], list)

        self.assertIn("Переводы и наличные", result["Расходы"])
        self.assertIsInstance(result["Расходы"]["Переводы и наличные"], list)

        self.assertIn("Поступления", result)
        self.assertEqual(result["Поступления"]["Общая сумма"], round(total_income))

        self.assertIn("Курс валют", result)
        self.assertEqual(result["Курс валют"], {'USD': 1.0})

        self.assertIn("Стоимость акций S&P500", result)
        self.assertEqual(result["Стоимость акций S&P500"], 4200.5)

    def test_main_function_with_mocked_data(self):
        # Можно добавить тест на конкретный вывод с конкретными моками
        pass


if __name__ == '__main__':
    unittest.main()