from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.utils.text import capfirst


def breadcrumbs(request):
    # Разбиваем путь на части
    path_parts = request.path.strip('/').split('/')

    # Начинаем с корня сайта
    breadcrumbs = [{'title': 'Home', 'url': '/home'}]
    current_path = ''

    for part in path_parts:
        current_path += f'/{part}'

        # Пробуем получить имя и параметры представления по текущему пути
        try:
            match = resolve(current_path)
            # Получаем название представления и преобразуем его в читаемый вид
            view_name = capfirst(match.view_name.split(':')[-1].replace('_', ' '))

            # Добавляем элемент хлебных крошек
            breadcrumbs.append({
                'title': view_name,
                'url': current_path
            })
        except Resolver404:
            # Если URL не найден, просто добавляем часть пути как есть
            breadcrumbs.append({
                'title': capfirst(part.replace('-', ' ')),
                'url': current_path
            })

    # Возвращаем breadcrumbs для использования в шаблоне
    return {'breadcrumbs': breadcrumbs}
