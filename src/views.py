from datetime import datetime
from django.http import JsonResponse


def main_page_view(request):
    """
    Обработка запроса для страницы 'Главная'.
    Ожидается, что дата и время передаются через GET-параметр 'datetime_str'.
    Формат строки: 'YYYY-MM-DD HH:MM:SS'
    """
    datetime_str = request.GET.get('datetime_str')
    if not datetime_str:
        return JsonResponse({'error': 'Параметр datetime_str обязателен'}, status=400)

    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        # Здесь можно выполнить любую обработку с объектом dt
        # Например, вернуть его в виде другого формата или вычислить что-то
        formatted_date = dt.strftime('%d.%m.%Y %H:%M:%S')
        return JsonResponse({'original': datetime_str, 'formatted': formatted_date})
    except ValueError:
        return JsonResponse({'error': 'Некорректный формат даты и времени'}, status=400)

