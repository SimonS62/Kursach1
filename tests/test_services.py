import unittest
import json
from datetime import datetime


# Определим CASHBACK_RATES для теста
CASHBACK_RATES = {
    'Продукты': 0.05,
    'Транспорт': 0.02,
    'Развлечения': 0.03,
    # Можно добавить другие категории по необходимости
}

class TestAnalyzeCashbackCategories(unittest.TestCase):

    def setUp(self):
        # Создаем список транзакций с датами, категориями и расходами
        self.data = [
            {'date': datetime(2023, 5, 10), 'category': 'Продукты', 'expenses': 100},
            {'date': datetime(2023, 5, 15), 'category': 'Транспорт', 'expenses': 50},
            {'date': datetime(2023, 5, 20), 'category': 'Развлечения', 'expenses': 200},
            {'date': datetime(2023, 4, 25), 'category': 'Продукты', 'expenses': 150},
            {'date': datetime(2023, 5, 5), 'category': 'Продукты', 'expenses': 50},
            {'date': datetime(2022, 5, 10), 'category': 'Транспорт', 'expenses': 70},
        ]

    def test_cashback_for_may_2023(self):
        result_json = analyze_cashback_categories(self.data, year=2023, month=5)
        result = json.loads(result_json)

        # Проверяем наличие категорий в результате
        self.assertIn('Продукты', result)
        self.assertIn('Транспорт', result)
        self.assertIn('Развлечения', result)

        # Проверяем правильность подсчета кешбэка
        # Расходы по категориям за май: Продукты=150 (100+50), Транспорт=50, Развлечения=200
        expected_cashback = {
            'Продукты': round(150 * CASHBACK_RATES['Продукты']),
            'Транспорт': round(50 * CASHBACK_RATES['Транспорт']),
            'Развлечения': round(200 * CASHBACK_RATES['Развлечения'])
        }
        self.assertEqual(result, expected_cashback)

    def test_no_transactions_in_month(self):
        # Месяц без транзакций
        result_json = analyze_cashback_categories(self.data, year=2021, month=1)
        result = json.loads(result_json)
        self.assertEqual(result, {})

    def test_category_without_rate(self):
        # Категория без заданного кешбэка в CASHBACK_RATES
        data = [
            {'date': datetime(2023, 6, 10), 'category': 'Неизвестная', 'expenses': 100}
        ]
        result_json = analyze_cashback_categories(data, year=2023, month=6)
        result = json.loads(result_json)
        # Кешбэк по категории без ставки должен быть нулём или отсутствовать?
        # В коде: get(cat,0) => кешбэк будет округлен к нулю.
        self.assertEqual(result.get('Неизвестная'), round(100 * CASHBACK_RATES.get('Неизвестная',0)))

if __name__ == '__main__':
    unittest.main()


class TestInvestSavings(unittest.TestCase):

    def setUp(self):
        # Создаем список транзакций с расходами
        self.transactions = [
            {'date': datetime(2024, 4, 10), 'category': 'Продукты', 'expenses': 123},
            {'date': datetime(2024, 4, 15), 'category': 'Транспорт', 'expenses': 47},
            {'date': datetime(2024, 4, 20), 'category': 'Развлечения', 'expenses': 200},
            {'date': datetime(2024, 4, 25), 'category': 'Подарки', 'expenses': 550},
            {'date': datetime(2024, 3, 30), 'category': 'Продукты', 'expenses': 300}
        ]

    def test_invest_savings_april(self):
        result_json = invest_savings(self.transactions, rounding_threshold=50)
        result = json.loads(result_json)

        # Проверяем общие траты
        total_spent = sum(t['expenses'] for t in self.transactions if t['date'].month == 4 and t['date'].year == 2024)
        self.assertEqual(result['Общие траты'], total_spent)

        # Проверяем сумму после округления
        # Расчеты по транзакциям за апрель:
        # 123 -> округление до 150 (разница +27)
        # 47 -> округление до 50 (разница +3)
        # 200 -> уже кратно 50 (разница 0)
        # 550 -> уже кратно (разница 0)
        expected_total_rounded = sum(
            ((t['expenses'] + 50 - 1) // 50) * 50 for t in self.transactions if
            t['date'].month == 4 and t['date'].year == 2024
        )
        self.assertEqual(result['Общая сумма после округления'], expected_total_rounded)

        # Проверяем накопленную сумму (сумма разниц)
        expected_difference = sum(
            (((t['expenses'] + 50 - 1) // 50) * 50 - t['expenses']) for t in self.transactions if
            t['date'].month == 4 and t['date'].year == 2024
        )
        self.assertAlmostEqual(result['Накопленная сумма на инвесткопилке'], expected_difference)

    def test_no_transactions_in_month(self):
        # Месяц без транзакций
        result_json = invest_savings(self.transactions, rounding_threshold=50)
        result = json.loads(result_json)

        # Проверка для месяца без транзакций (например, май)
        april_transactions = [t for t in self.transactions if t['date'].month == 5]
        total_spent_april = sum(t['expenses'] for t in april_transactions)

        self.assertEqual(result['Общие траты'], total_spent_april)

    def test_different_rounding_threshold(self):
        result_json = invest_savings(self.transactions, rounding_threshold=100)
        result = json.loads(result_json)

        # Проверка суммы после округления с порогом 100
        total_rounded = sum(
            ((t['expenses'] + 100 - 1) // 100) * 100 for t in self.transactions if
            t['date'].month == 4 and t['date'].year == 2024
        )

        self.assertEqual(result['Общая сумма после округления'], total_rounded)


if __name__ == '__main__':
    unittest.main()