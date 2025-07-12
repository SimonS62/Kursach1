import unittest
import os
import json
from unittest.mock import patch


# Для теста создадим простую функцию, задекорированную этим декоратором
@save_report()
def sample_function():
    return {'status': 'success', 'data': [1, 2, 3]}


class TestSaveReportDecorator(unittest.TestCase):

    def setUp(self):
        # Очистка файлов перед каждым тестом
        self.filename = 'sample_function.json'
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        # Удаление файла после теста, если он остался
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_file_creation_and_content(self):
        # Вызов функции, задекорированной save_report
        result = sample_function()

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.filename), "Файл не был создан.")

        # Проверяем содержимое файла
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data, {'status': 'success', 'data': [1, 2, 3]})

        # Проверяем возвращаемое значение функции совпадает с результатом
        self.assertEqual(result, {'status': 'success', 'data': [1, 2, 3]})

    @patch('builtins.open')
    def test_error_handling_in_file_write(self, mock_open):
        # Имитируем ошибку при открытии файла
        mock_open.side_effect = IOError("Ошибка открытия файла")

        # Создаем функцию с декоратором с явно указанным именем файла
        @save_report('test_error.json')
        def faulty_function():
            return {'error': True}

        result = faulty_function()

        # В случае ошибки функция должна вернуть результат без исключения
        self.assertEqual(result, {'error': True})

    @patch('json.dump')
    def test_json_dump_called_with_correct_args(self, mock_json_dump):
        # Проверка вызова json.dump с правильными аргументами
        sample_function()

        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args

        # Первый аргумент - результат функции (словарь)
        self.assertIsInstance(args[0], dict)

        # Второй аргумент - файл (объект)
        self.assertTrue(hasattr(args[1], 'write'))


# Запуск тестов
if __name__ == '__main__':
    unittest.main()


class TestParseDate(unittest.TestCase):

    def test_parse_valid_date_string(self):
        date_str = '2024-04-27'
        result = parse_date(date_str)
        expected = datetime(2024, 4, 27)
        self.assertEqual(result.year, expected.year)
        self.assertEqual(result.month, expected.month)
        self.assertEqual(result.day, expected.day)

    def test_parse_invalid_date_string_returns_now(self):
        invalid_date_str = 'invalid-date'
        result = parse_date(invalid_date_str)
        now = datetime.now()
        # Проверяем, что возвращается примерно сейчас (с учетом времени выполнения теста)
        self.assertAlmostEqual(result.year, now.year, delta=1)
        self.assertAlmostEqual(result.month, now.month, delta=1)
        self.assertAlmostEqual(result.day, now.day, delta=1)

    def test_parse_none_returns_now(self):
        result = parse_date(None)
        now = datetime.now()
        # Проверяем, что возвращается текущая дата
        self.assertAlmostEqual(result.year, now.year, delta=1)
        self.assertAlmostEqual(result.month, now.month, delta=1)
        self.assertAlmostEqual(result.day, now.day, delta=1)

if __name__ == '__main__':
    unittest.main()


class TestSpendingByCategory(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.transactions = pd.DataFrame({
            'date': [
                datetime(2024, 1, 15),
                datetime(2024, 2, 10),
                datetime(2024, 3, 5),
                datetime(2024, 3, 20),
                datetime(2024, 4, 1)
            ],
            'category': ['food', 'food', 'entertainment', 'food', 'utilities'],
            'amount': [50.0, 20.0, 100.0, 30.0, 200.0]
        })

    def test_spending_last_3_months_for_food(self):
        # Текущая дата - апрель 2024 (фиксируем дату)
        date_str = '2024-04-01'
        result = spending_by_category(self.transactions, 'food', date=date_str)

        # Расчет ожидаемых значений
        # За последние 3 месяца от 2024-04-01: январь-март
        expected_total = 50.0 + 20.0 + 30.0
        expected_start_date = '2024-01-01'   # три месяца назад от 2024-04-01
        expected_end_date = '2024-04-01'

        self.assertEqual(result['category'], 'food')
        self.assertEqual(result['start_date'], expected_start_date)
        self.assertEqual(result['end_date'], expected_end_date)
        self.assertAlmostEqual(result['total_expenses'], expected_total)
        self.assertEqual(result['transactions_count'], 3)

    def test_no_transactions_in_period(self):
        # Проверка для категории без транзакций в периоде
        result = spending_by_category(self.transactions, 'utilities', date='2024-02-01')
        self.assertEqual(result['total_expenses'], 0)
        self.assertEqual(result['transactions_count'], 0)

if __name__ == '__main__':
    unittest.main()


class TestSpendingByWeekday(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.transactions = pd.DataFrame({
            'date': [
                datetime(2024, 1, 1),   # Monday
                datetime(2024, 1, 2),   # Tuesday
                datetime(2024, 1, 3),   # Wednesday
                datetime(2024, 1, 4),   # Thursday
                datetime(2024, 1, 5),   # Friday
                datetime(2024, 1, 6),   # Saturday
                datetime(2024, 1, 7),   # Sunday
                datetime(2024, 2, 14),  # Wednesday
                datetime(2024, 2, 15),  # Thursday
            ],
            'amount': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
        })

    def test_average_spending_per_weekday(self):
        date_str = '2024-04-01'
        result = spending_by_weekday(self.transactions, date=date_str)

        # Проверяем средние значения по дням недели
        expected = {
            'Monday': 0,
            'Tuesday': 20.0,
            'Wednesday': (30.0 + 80.0) /2,
            'Thursday': (40.0 +90.0)/2,
            'Friday':50.0,
            'Saturday':60.0,
            'Sunday':70.0
        }

        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            self.assertAlmostEqual(result[day], expected[day], places=2)

if __name__ == '__main__':
    unittest.main()


class TestSpendingByWorkday(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.transactions = pd.DataFrame({
            'date': [
                datetime(2024, 1, 1),   # Monday (выходной)
                datetime(2024, 1, 2),   # Tuesday (рабочий)
                datetime(2024, 1, 5),   # Friday (рабочий)
                datetime(2024, 1, 6),   # Saturday (выходной)
                datetime(2024, 2, 14),  # Wednesday (рабочий)
                datetime(2024, 2, 17),  # Saturday (выходной)
                datetime(2024, 3, 1),   # Friday (рабочий)
            ],
            'amount': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0]
        })

    def test_average_expenses_work_and_weekend(self):
        date_str = '2024-04-01'
        result = spending_by_workday(self.transactions, date=date_str)

        # Расчет ожидаемых средних значений
        # В период попадают все транзакции за январь-март
        work_expenses = [20.0,30.0,50.0,70.0]
        weekend_expenses = [10.0,40.0,60.0]

        expected_work_avg = sum(work_expenses) / len(work_expenses)
        expected_weekend_avg = sum(weekend_expenses) / len(weekend_expenses)

        self.assertAlmostEqual(result['workdays_avg_expense'], expected_work_avg)
        self.assertAlmostEqual(result['weekend_avg_expense'], expected_weekend_avg)

    def test_no_transactions_in_period(self):
        # Тестируем случай без транзакций в периоде
        empty_transactions = pd.DataFrame({'date': [], 'amount': []})
        result = spending_by_workday(empty_transactions, date='2024-04-01')
        self.assertEqual(result['workdays_avg_expense'], 0.0)
        self.assertEqual(result['weekend_avg_expense'], 0.0)

if __name__ == '__main__':
    unittest.main()
