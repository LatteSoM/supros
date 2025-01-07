from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.utils.text import capfirst


# def breadcrumbs(request):
#     # Разбиваем путь на части
#     path_parts = request.path.strip('/').split('/')
#
#     # Начинаем с корня сайта
#     breadcrumbs = [{'title': 'Home', 'url': '/home'}]
#     current_path = ''
#
#     for part in path_parts:
#         current_path += f'/{part}'
#
#         # Пробуем получить имя и параметры представления по текущему пути
#         try:
#             match = resolve(current_path)
#             # Получаем название представления и преобразуем его в читаемый вид
#             view_name = capfirst(match.view_name.split(':')[-1].replace('_', ' '))
#
#             # Добавляем элемент хлебных крошек
#             breadcrumbs.append({
#                 'title': view_name,
#                 'url': current_path
#             })
#         except Resolver404:
#             # Если URL не найден, просто добавляем часть пути как есть
#             breadcrumbs.append({
#                 'title': capfirst(part.replace('-', ' ')),
#                 'url': current_path
#             })
#
#     # Возвращаем breadcrumbs для использования в шаблоне
#     return {'breadcrumbs': breadcrumbs}


from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.utils.text import capfirst

# Словарь перевода маршрутов
ROUTE_TRANSLATIONS = {
    'home': 'Главная',
    'forbidden': 'Доступ запрещён',
    'export_csv': 'Экспорт CSV',
    'export_sql': 'Экспорт SQL',
    'login': 'Вход',
    'logout': 'Выход',
    'reestr': 'Реестр',
    'deps': 'Отделы',
    'projects': 'Проекты',
    'tasks': 'Задачи',
    'tasks_user': 'Мои задачи',
    'settings': 'Настройки',
    'departments': 'Подразделения',
    'roles': 'Роли',
    'document_type': 'Типы документов',
    'document': 'Документы',
    'employee': 'Сотрудники',
    'employee_reestr': 'Добавить сотрудника в реестр',
    'user': 'Пользователи',
    'position': 'Должности',
    'emp_position': 'Позиции сотрудников',
    'worktime': 'Рабочее время',
    'my-work-time': 'Моё рабочее время',
    'project': 'Проект',
    'task': 'Задача',
    'payroll': 'Зарплаты',
    'add': 'Добавить',
    'edit': 'Редактировать',
    'delete': 'Удалить',
    'detail': 'Детали',
    'remove_employee': 'Удалить сотрудника',
    'confirm': 'Подтвердить',
}


def breadcrumbs(request):
    # Разбиваем путь на части
    path_parts = request.path.strip('/').split('/')

    # Начинаем с корня сайта
    breadcrumbs = [{'title': ROUTE_TRANSLATIONS.get('home', 'Главная'), 'url': '/home'}]
    current_path = ''

    for part in path_parts:
        current_path += f'/{part}'

        # Пробуем получить имя и параметры представления по текущему пути
        try:
            match = resolve(current_path)
            view_name = match.view_name.split(':')[-1].replace('_', ' ')

            # Переводим имя маршрута, если оно есть в словаре
            translated_name = ROUTE_TRANSLATIONS.get(part, capfirst(part.replace('-', ' ')))

            # Добавляем элемент хлебных крошек
            breadcrumbs.append({
                'title': translated_name,
                'url': current_path
            })
        except Resolver404:
            # Если URL не найден, добавляем как есть, с переводом при наличии
            translated_part = ROUTE_TRANSLATIONS.get(part, capfirst(part.replace('-', ' ')))
            breadcrumbs.append({
                'title': translated_part,
                'url': current_path
            })

    return {'breadcrumbs': breadcrumbs}

