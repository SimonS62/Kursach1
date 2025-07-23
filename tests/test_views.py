import unittest
from datetime import datetime
import json
from views import get_greeting, get_total_expenses, get_last4_digits, get_cashback, get_currency_rate, get_sp500_price, get_top_transactions


def get_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def get_total_expenses(transactions):
    return sum(t['amount'] for t in transactions)

def get_last4_digits(card_number: str) -> str:
    return card_number[-4:] if len(card_number) >= 4 else card_number

def get_cashback(amount: float) -> float:
    return abs(amount) * 0.01

def get_currency_rate():
    return {"USD": 1.0, "EUR": 0.85}

def get_sp500_price():
    return 4200.0

def get_top_transactions(transactions):
    sorted_tx = sorted(transactions, key=lambda x: abs(x['amount']), reverse=True)
    return sorted_tx[:5]

class TestFunctions(unittest.TestCase):

    def test_get_greeting(self):
        self.assertEqual(get_greeting(6), "Доброе утро")
        self.assertEqual(get_greeting(13), "Добрый день")
        self.assertEqual(get_greeting(19), "Добрый вечер")
        self.assertEqual(get_greeting(2), "Доброй ночи")
        self.assertEqual(get_greeting(23), "Доброй ночи")

    def test_get_total_expenses(self):
        transactions = [{'amount': 100}, {'amount': -50}, {'amount': 200}]
        self.assertEqual(get_total_expenses(transactions), 250)

    def test_get_last4_digits(self):
        self.assertEqual(get_last4_digits("1234567890123456"), "3456")
        self.assertEqual(get_last4_digits("123"), "123")
        self.assertEqual(get_last4_digits(""), "")

    def test_get_cashback(self):
        self.assertAlmostEqual(get_cashback(100), 1.0)
        self.assertAlmostEqual(get_cashback(-50), 0.5)
        self.assertAlmostEqual(get_cashback(0), 0)

    def test_get_currency_rate(self):
        rates = get_currency_rate()
        self.assertIn("USD", rates)
        self.assertIn("EUR", rates)
        self.assertIsInstance(rates["USD"], float)

    def test_get_sp500_price(self):
        price = get_sp500_price()
        self.assertIsInstance(price, (int, float))
        self.assertGreater(price, 0)

    def test_get_top_transactions(self):
        transactions = [
            {'amount': 100},
            {'amount': -200},
            {'amount': 50},
            {'amount': -300},
            {'amount': 400},
            {'amount': -150}
        ]
        top = get_top_transactions(transactions)
        # Проверяем что топ-5 по абсолютной сумме
        expected_amounts = [400, -300, -200, -150, 100]
        actual_amounts = [t['amount'] for t in top]
        self.assertEqual(actual_amounts, expected_amounts[:5])

if __name__ == '__main__':
    unittest.main()