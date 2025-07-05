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

    # Предполагается, что транзакции имеют колонки: 'date' (datetime), 'category' (str), 'amount' (float)
    df_filtered = transactions[
        (transactions['date'] >= start_date) &
        (transactions['date'] <= end_date) &
        (transactions['category'] == category)
        ]

    total_expenses = df_filtered['amount'].sum()

    result = {
        'category': category,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_expenses': total_expenses,
        'transactions_count': len(df_filtered)
    }
    return result


@save_report()
def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> dict:
    """
    Возвращает средние траты в каждый из дней недели за последние 3 месяца.
    """
    end_date = parse_date(date)
    start_date = end_date - pd.DateOffset(months=3)

    df_filtered = transactions[
        (transactions['date'] >= start_date) &
        (transactions['date'] <= end_date)
        ].copy()

    # Добавляем колонку с днем недели
    df_filtered['weekday'] = df_filtered['date'].dt.day_name()

    # Группируем по дню недели и считаем средний расход
    grouped = df_filtered.groupby('weekday')['amount'].mean()

    # Порядок дней недели для вывода
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Создаем результат с учетом порядка дней
    result = {day: float(grouped.get(day, 0)) for day in days_order}

    return result


@save_report()
def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> dict:
    """
    Возвращает средние траты в рабочие и выходные дни за последние 3 месяца.
    """
    end_date = parse_date(date)
    start_date = end_date - pd.DateOffset(months=3)

    df_filtered = transactions[
        (transactions['date'] >= start_date) &
        (transactions['date'] <= end_date)
        ].copy()

    # Добавляем колонку с днем недели
    df_filtered['weekday'] = df_filtered['date'].dt.day_name()

    # Определяем рабочие и выходные дни
    workdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    workday_expenses_series = df_filtered[df_filtered['weekday'].isin(workdays)]['amount']

    weekend_expenses_series = df_filtered[~df_filtered['weekday'].isin(workdays)]['amount']

    workday_avg = float(workday_expenses_series.mean()) if not workday_expenses_series.empty else 0.0


weekend_avg = float(weekend_expenses_series.mean()) if not weekend_expenses_series.empty else 0.0

result = {
    'workdays_avg_expense': workday_avg,
    'weekend_avg_expense': weekend_avg,
    'period_start': start_date.strftime('%Y-%m-%d'),
    'period_end': end_date.strftime('%Y-%m-%d')
}
return result

