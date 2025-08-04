import unittest
import pandas as pd
import os
import json
from datetime import datetime
from reports import spending_by_category, save_report


class TestSpendingByCategory(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные DataFrame
        data = {
            'Дата операции': [
                datetime(2021, 8, 15),
                datetime(2021, 9, 10),
                datetime(2021, 10, 5),
                datetime(2021, 11, 5),
                datetime(2021, 11, 10),
            ],
            'Категория': [
                'Фастфуд',
                'Фастфуд',
                'Фастфуд',
                'Фастфуд',
                'Кафе'
            ],
            'Сумма операции': [
                -500,
                -300,
                -200,
                -100,
                -50
            ]
        }
        self.df = pd.DataFrame(data)

    def test_spending_last_3_months(self):
        # Проверка подсчета расходов за последние 3 месяца от 2021-11-10
        result = spending_by_category(self.df, 'Фастфуд', "2021-11-10")
        # Ожидается сумма: -200 + -100 = -300 (т.к. только эти попадают в диапазон)
        self.assertEqual(result['category'], 'Фастфуд')
        self.assertEqual(result['start_date'], '2021-08-10')  # три месяца назад от 2021-11-10
        self.assertEqual(result['end_date'], '2021-11-10')
        self.assertEqual(result['transactions_count'], 2)
        self.assertEqual(result['total_expenses'], -300)

    def test_save_report_decorator_creates_file(self):
        # Проверка, что декоратор сохраняет файл
        filename = 'test_report.json'

        @save_report(filename)
        def dummy_func():
            return {'test': True}

        # Удаляем файл если он есть
        if os.path.exists(filename):
            os.remove(filename)

        result = dummy_func()
        self.assertTrue(os.path.exists(filename))

        # Проверяем содержимое файла
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(data, {'test': True})

        # Удаляем файл после теста
        os.remove(filename)

    def test_parse_date_none_returns_now(self):
        dt_now = datetime.now()
        parsed_date = parse_date(None)
        # Проверяем что возвращается дата не раньше текущего времени (с учетом времени выполнения)
        self.assertTrue(parsed_date >= dt_now)

    def test_parse_date_invalid_format(self):
        date_str = "invalid-date"
        parsed_date = parse_date(date_str)
        dt_now = datetime.now()
        self.assertTrue(parsed_date >= dt_now)


if __name__ == '__main__':
    unittest.main()