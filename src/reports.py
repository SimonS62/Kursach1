import json
import pandas as pd
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('reports.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результата функции в файл.
    Если filename не указан, используется имя функции + '.json'.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_name = filename or f"{func.__name__}.json"
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info(f"Отчет '{file_name}' успешно сохранен.")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета '{file_name}': {e}")
            return result

        return wrapper

    return decorator


def parse_date(date_str: Optional[str]) -> datetime:
    """
    Вспомогательная функция для парсинга даты из строки или возврата текущей даты.
    """
    if date_str is None:
        return datetime.now()
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        # Можно расширить обработку ошибок при необходимости
        return datetime.now()


@save_report()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> dict:
    """
    Возвращает траты по заданной категории за последние 3 месяца от указанной даты.
    """
    end_date = parse_date(date)
    start_date = end_date - pd.DateOffset(months=3)

    # Транзакции имеют колонки: 'Дата операции' (datetime), 'Категория' (str), 'Сумма операции' (float)
    df_filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date) &
        (transactions['Категория'] == category) &
        (transactions['Сумма операции'] < 0)
        ]

    total_expenses = df_filtered['Сумма операции'].sum()

    result = {
        'category': category,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_expenses': total_expenses,
        'transactions_count': len(df_filtered)
    }
    return result

if __name__ == '__main__':
    data = pd.read_excel('../data/operations.xlsx', parse_dates=['Дата операции'])
    result = spending_by_category(data, 'Фастфуд', "2021-11-10")
    print(result)
