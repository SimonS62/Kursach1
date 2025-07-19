import unittest
from datetime import datetime
import json


class TestAnalyzeCashbackCategories(unittest.TestCase):

    def setUp(self):
        # Пример данных для теста
        self.transactions = [
            {'Дата операции': datetime(2021, 11, 10), 'Категория': 'Продукты', 'Сумма операции': 123},
            {'Дата операции': datetime(2021, 11, 15), 'Категория': 'Транспорт', 'Сумма операции': 47},
            {'Дата операции': datetime(2021, 11, 20), 'Категория': 'Развлечения', 'Сумма операции': 200},
            {'Дата операции': datetime(2021, 11, 25), 'Категория': 'Подарки', 'Сумма операции': 550},
            {'Дата операции': datetime(2021, 11, 30), 'Категория': 'Продукты', 'Сумма операции': 300}
        ]

    def test_analyze_cashback_categories_november(self):
        result_json = analyze_cashback_categories(self.transactions, 2021, 11)
        result = json.loads(result_json)

        # Проверяем наличие всех категорий
        self.assertIn('Продукты', result)
        self.assertIn('Транспорт', result)
        self.assertIn('Развлечения', result)
        self.assertIn('Подарки', result)

        # Проверяем правильность расчетов кешбэка
        # Продукты: сумма = 123 + 300 = 423; кешбэк = round(423 * 0.05) = round(21.15) = 21
        self.assertEqual(result['Продукты'], 21)

        # Транспорт: сумма = 47; кешбэк = round(47 * 0.02) = round(0.94) = 1
        self.assertEqual(result['Транспорт'], 1)

        # Развлечения: сумма = 200; кешбэк = round(200 * 0.03) = round(6) =6
        self.assertEqual(result['Развлечения'], 6)

        # Подарки: сумма=550; кешбэк=round(550*0.04)=round(22)=22
        self.assertEqual(result['Подарки'], 22)

    def test_no_transactions_for_month(self):
        # Транзакции за другой месяц — результат должен быть пустым
        result_json = analyze_cashback_categories(self.transactions, 2022, 12)
        result = json.loads(result_json)
        self.assertEqual(result, {})

    def test_unknown_category(self):
        # Добавим транзакцию с новой категорией без ставки кешбэка
        transactions = self.transactions + [
            {'Дата операции': datetime(2021, 11, 10), 'Категория': 'Новая категория', 'Сумма операции': 100}
        ]
        result_json = analyze_cashback_categories(transactions, 2021, 11)
        result = json.loads(result_json)

        # Для новой категории ставка равна нулю
        self.assertEqual(result.get('Новая категория'), None or False)

    def test_rounding(self):
        # Проверка округления (например сумма=2.5 при ставке=0.05 даст кешбэк=0)
        transactions = [
            {'Дата операции': datetime(2021, 11, 10), 'Категория': 'Продукты', 'Сумма операции': 50}
        ]
        result_json = analyze_cashback_categories(transactions, 2021, 11)
        result = json.loads(result_json)

        # Расчет: round(50*0.05)=round(2.5)=3 (по правилам Python)
        self.assertEqual(result['Продукты'], 3)


if __name__ == '__main__':
    unittest.main()
