import unittest
from datetime import datetime, timedelta


class TestGetGreeting(unittest.TestCase):

    def test_morning(self):
        # Проверка утренних часов (5-11)
        self.assertEqual(get_greeting(5), "Доброе утро")
        self.assertEqual(get_greeting(11), "Доброе утро")
        # Проверка границы
        self.assertEqual(get_greeting(6), "Доброе утро")
        self.assertEqual(get_greeting(10), "Доброе утро")

    def test_day(self):
        # Проверка дневных часов (12-16)
        self.assertEqual(get_greeting(12), "Добрый день")
        self.assertEqual(get_greeting(16), "Добрый день")

    def test_evening(self):
        # Проверка вечерних часов (17-22)
        self.assertEqual(get_greeting(17), "Добрый вечер")
        self.assertEqual(get_greeting(22), "Добрый вечер")

    def test_night(self):
        # Проверка ночных часов (0-4 и 23-24)
        self.assertEqual(get_greeting(0), "Доброй ночи")
        self.assertEqual(get_greeting(4), "Доброй ночи")
        self.assertEqual(get_greeting(23), "Доброй ночи")
        # Также проверим границы
        self.assertEqual(get_greeting(24), "Доброй ночи")  # если 24 возможен, зависит от контекста

if __name__ == '__main__':
    unittest.main()


class TestFunctions(unittest.TestCase):

    def test_get_last4_digits(self):
        # Проверка получения последних 4 цифр
        self.assertEqual(get_last4_digits("1234567890123456"), "3456")
        self.assertEqual(get_last4_digits("987654321"), "4321")
        self.assertEqual(get_last4_digits("0000"), "0000")
        # Проверка короткого номера (если есть такие случаи)
        self.assertEqual(get_last4_digits("123"), "123")  # возвращает все, если длина меньше 4

    def test_get_total_expenses(self):
        # Проверка суммы транзакций
        transactions = [
            {'amount': 100},
            {'amount': 250},
            {'amount': -50},  # допустимо, если есть возвраты
            {'amount': 300}
        ]
        self.assertEqual(get_total_expenses(transactions), 100 + 250 - 50 + 300)

        # Тест с пустым списком
        self.assertEqual(get_total_expenses([]), 0)

    def test_get_cashback(self):
        # Проверка кешбэка
        self.assertEqual(get_cashback(0), 0)
        self.assertEqual(get_cashback(99), 0)
        self.assertEqual(get_cashback(100), 1)
        self.assertEqual(get_cashback(250), 2)
        self.assertEqual(get_cashback(999), 9)
        self.assertEqual(get_cashback(1000), 10)

if __name__ == '__main__':
    unittest.main()


class TestFinancialFunctions(unittest.TestCase):

    def test_get_top_transactions(self):
        transactions = [
            {'amount': 1000},
            {'amount': 2500},
            {'amount': 1500},
            {'amount': 3000},
            {'amount': 2000},
            {'amount': 500}
        ]
        top_3 = get_top_transactions(transactions, top_n=3)
        # Проверяем, что возвращаются топ-3 по сумме
        self.assertEqual(len(top_3), 3)
        # Проверяем, что они отсортированы по убыванию
        amounts = [t['amount'] for t in top_3]
        self.assertTrue(all(amounts[i] >= amounts[i+1] for i in range(len(amounts)-1)))
        # Проверяем правильность выбора верхних транзакций
        expected_amounts = sorted([t['amount'] for t in transactions], reverse=True)[:3]
        self.assertEqual(amounts, expected_amounts)

    def test_get_currency_rate(self):
        rates = get_currency_rate()
        # Проверяем наличие ключей и тип значений
        self.assertIn('USD', rates)
        self.assertIn('EUR', rates)
        self.assertIn('RUB', rates)
        self.assertIsInstance(rates['USD'], float)
        self.assertIsInstance(rates['EUR'], float)
        self.assertIsInstance(rates['RUB'], float)
        # Проверка значений
        self.assertEqual(rates['RUB'], 1.0)

    def test_get_sp500_price(self):
        price = get_sp500_price()
        # Проверка типа и значения
        self.assertIsInstance(price, float)
        self.assertEqual(price, 4200.50)

if __name__ == '__main__':
    unittest.main()


class TestGetDateRange(unittest.TestCase):

    def test_all_range(self):
        date_str = '2023-08-15 14:30:00'
        start, end = get_date_range(date_str, 'ALL')
        self.assertEqual(start, datetime(2000, 1, 1))
        self.assertEqual(end, datetime(2023, 8, 15, 14, 30, 0))

    def test_week_range(self):
        date_str = '2023-08-15 14:30:00'
        start, end = get_date_range(date_str, 'W')
        expected_end = datetime(2023, 8, 15, 14, 30, 0)
        expected_start = expected_end - timedelta(days=6)
        self.assertEqual(end, expected_end)
        self.assertEqual(start.date(), expected_start.date())

    def test_month_range(self):
        date_str = '2023-08-15 14:30:00'
        start, end = get_date_range(date_str, 'M')
        self.assertEqual(start, datetime(2023, 8, 1))
        self.assertEqual(end, datetime(2023, 8, 15, 14, 30, 0))

    def test_year_range(self):
        date_str = '2023-08-15 14:30:00'
        start, end = get_date_range(date_str, 'Y')
        self.assertEqual(start, datetime(2023, 1, 1))
        self.assertEqual(end, datetime(2023, 8, 15, 14, 30))

    def test_default_range(self):
        # Если передать неизвестный тип — по умолчанию месяц
        date_str = '2023-08-15 14:30:00'
        start, end = get_date_range(date_str)
        self.assertEqual(start, datetime(2023, 8, 1))
        self.assertEqual(end.date(), datetime(2023, 8, 15).date())


if __name__ == '__main__':
    unittest.main()


class TestFilterTransactions(unittest.TestCase):

    def setUp(self):
        # Создаем список транзакций с разными датами
        self.transactions = [
            {'id': 1, 'amount': 100, 'date': datetime(2023, 8, 10, 12, 0)},
            {'id': 2, 'amount': 200, 'date': datetime(2023, 8, 15, 15, 30)},
            {'id': 3, 'amount': 300, 'date': datetime(2023, 8, 20, 9, 45)},
            {'id': 4, 'amount': 400, 'date': datetime(2023, 8, 25, 18, 0)},
        ]

    def test_filter_inclusive(self):
        start_date = datetime(2023, 8, 15)
        end_date = datetime(2023, 8, 25)
        filtered = filter_transactions(self.transactions, start_date, end_date)
        # Должны остаться транзакции с датами от 15 до 25 августа включительно
        expected_ids = {2, 3, 4}
        result_ids = {t['id'] for t in filtered}
        self.assertEqual(result_ids, expected_ids)

    def test_filter_single_day(self):
        start_date = datetime(2023, 8, 20)
        end_date = datetime(2023, 8, 20)
        filtered = filter_transactions(self.transactions, start_date, end_date)
        # Только транзакция с датой ровно на этот день
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['id'], 3)

    def test_filter_no_matches(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        filtered = filter_transactions(self.transactions, start_date, end_date)
        self.assertEqual(filtered, len(filtered))

    def test_filter_all(self):
        start_date = datetime(2023, 8, 10)
        end_date = datetime(2023, 8, 25)
        filtered = filter_transactions(self.transactions, start_date, end_date)
        self.assertEqual(len(filtered), 4)


if __name__ == '__main__':
    unittest.main()


class TestGetTopCategories(unittest.TestCase):

    def setUp(self):
        # Создаем список транзакций с категориями и суммами доходов/расходов
        self.transactions = [
            {'category': 'Продукты', 'expenses': 150.75, 'income': 0},
            {'category': 'Транспорт', 'expenses': 50.25, 'income': 0},
            {'category': 'Развлечения', 'expenses': 200.50, 'income': 0},
            {'category': 'Продукты', 'expenses': 100.25, 'income': 0},
            {'category': 'Зарплата', 'expenses': 0, 'income': 3000},
            {'category': 'Фриланс', 'expenses': 0, 'income': 500},
            {'category': 'Транспорт', 'expenses': 25.75, 'income': 0},
        ]

    def test_top_expenses(self):
        result = get_top_categories(self.transactions, key='expenses', top_n=3)
        # Проверяем что возвращается список из топ-3 + "Остальное"
        categories = [item['category'] for item in result]
        self.assertIn('Продукты', categories)
        self.assertIn('Транспорт', categories)
        self.assertIn('Развлечения', categories)
        self.assertIn('Остальное', categories)
        # Проверяем сумму "Остальное" равна сумме остальных категорий
        total_expenses = sum(t['expenses'] for t in self.transactions)
        sum_top = sum(item['amount'] for item in result if item['category'] != 'Остальное')
        sum_other = next(item['amount'] for item in result if item['category'] == 'Остальное')
        self.assertAlmostEqual(sum_top + sum_other, round(total_expenses))

    def test_top_income(self):
        result = get_top_categories(self.transactions, key='income', top_n=2)
        categories = [item['category'] for item in result]
        self.assertIn('Зарплата', categories)
        self.assertIn('Фриланс', categories)
        self.assertIn('Остальное', categories)

    def test_less_than_top_n_categories(self):
        # Если категорий меньше чем top_n
        transactions = [
            {'category': 'A', 'expenses': 100, 'income': 0},
            {'category': 'B', 'expenses': 200, 'income': 0}
        ]
        result = get_top_categories(transactions, key='expenses', top_n=5)
        categories = [item['category'] for item in result]
        self.assertIn('A', categories)
        self.assertIn('B', categories)
        # Остальных нет, значит "Остальное" не должно быть
        self.assertNotIn('Остальное', categories)


if __name__ == '__main__':
    unittest.main()


class TestGetExpensesAndIncome(unittest.TestCase):

    def setUp(self):
        # Создаем список транзакций с расходами и доходами
        self.transactions = [
            {'expenses': 150.75, 'income': 0},
            {'expenses': 50.25, 'income': 0},
            {'expenses': 200.50, 'income': 0},
            {'expenses': 100.25, 'income': 3000},
            {'expenses': 0, 'income': 500},
            {'expenses': 25.75, 'income': 0},
        ]

    def test_total_expenses_and_income(self):
        total_expenses, total_income = get_expenses_and_income(self.transactions)
        expected_expenses = sum(t['expenses'] for t in self.transactions)
        expected_income = sum(t['income'] for t in self.transactions)
        self.assertEqual(total_expenses, round(expected_expenses))
        self.assertEqual(total_income, round(expected_income))

    def test_zero_transactions(self):
        transactions = []
        expenses, income = get_expenses_and_income(transactions)
        self.assertEqual(expenses, 0)
        self.assertEqual(income, 0)

    def test_only_expenses(self):
        transactions = [
            {'expenses': 100.4, 'income': 0},
            {'expenses': 200.6, 'income': 0}
        ]
        expenses, income = get_expenses_and_income(transactions)
        self.assertEqual(expenses, round(100.4 + 200.6))
        self.assertEqual(income, 0)

    def test_only_income(self):
        transactions = [
            {'expenses': 0, 'income': 100.4},
            {'expenses': 0, 'income': 200.6}
        ]
        expenses, income = get_expenses_and_income(transactions)
        self.assertEqual(expenses, 0)
        self.assertEqual(income, round(100.4 + 200.6))


if __name__ == '__main__':
    unittest.main()


class TestStaticFunctions(unittest.TestCase):

    def test_get_currency_rate(self):
        rates = get_currency_rate()
        # Проверяем наличие ключей
        self.assertIn('USD', rates)
        self.assertIn('EUR', rates)
        self.assertIn('RUB', rates)
        # Проверяем значения
        self.assertEqual(rates['USD'], 75.0)
        self.assertEqual(rates['EUR'], 88.0)
        self.assertEqual(rates['RUB'], 1.0)

    def test_get_sp500_price(self):
        price = get_sp500_price()
        # Проверяем тип и значение
        self.assertIsInstance(price, float)
        self.assertEqual(price, 4200.50)

if __name__ == '__main__':
    unittest.main()
