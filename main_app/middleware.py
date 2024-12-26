from decimal import Decimal

import pytz
from django.conf import settings
from django.shortcuts import redirect

import datetime
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from main_app.models import WorkTime, Employee
from django.utils.timezone import make_aware, is_naive, timezone


EXCLUDED_URLS = ['/login/', '/logout/']


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in EXCLUDED_URLS:
            return redirect('login')
        return self.get_response(request)


import logging

logger = logging.getLogger(__name__)


class WorkTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # if request.user.is_authenticated:
        #     logger.info(f"User {request.user.username} is authenticated.")
        #     self.track_work_time(request)

        return response


    def track_work_time(self, request):
        if 'login_time' in request.session:
            login_time_str = request.session['login_time']
            # Преобразуем строку в datetime
            try:
                login_time = datetime.datetime.fromisoformat(login_time_str)  # Преобразуем строку в datetime
            except ValueError:
                logger.error(f"Invalid login time format: {login_time_str}")
                return

            # Привязываем к временному поясу (например, UTC)
            if is_naive(login_time):  # Проверяем, если время не имеет часового пояса
                login_time = make_aware(login_time, timezone=pytz.UTC)  # Привязываем к часовому поясу UTC

            logout_time = now()  # Время выхода

            # Рассчитываем продолжительность сессии
            session_duration = (logout_time - login_time).total_seconds() / 3600.0
            session_duration = Decimal(session_duration).quantize(Decimal('0.01'))

            logger.info(f"Tracking work time for user {request.user.username}: {session_duration} hours.")

            # Обновляем рабочее время
            work_time, created = WorkTime.objects.get_or_create(
                employee=request.user.employee,
                date=now().date(),
                defaults={'hours_worked': 0}
            )
            work_time.hours_worked += session_duration
            work_time.save()

            # Удаляем login_time из сессии
            request.session.pop('login_time', None)

    # def track_work_time(self, request):
    #     if 'login_time' in request.session:
    #         login_time = request.session['login_time']
    #
    #         # Убедиться, что время имеет привязку к часовому поясу
    #         if is_naive(login_time):
    #             login_time = make_aware(login_time, timezone=pytz.UTC)
    #
    #         # Текущее время выхода
    #         logout_time = now()
    #
    #         # Рассчитать продолжительность сессии
    #         session_duration = (logout_time - login_time).total_seconds() / 3600.0
    #         logger.info(f"Tracking work time for user {request.user.username}: {session_duration} hours.")
    #
    #         session_duration = Decimal(session_duration).quantize(Decimal('0.01'))
    #
    #         logger.info(f"Tracking work time for user {request.user.username}: {session_duration} hours.")
    #
    #         # Обновить рабочее время в базе данных
    #         work_time, created = WorkTime.objects.get_or_create(
    #             employee=request.user.employee,
    #             date=now().date(),
    #             defaults={'hours_worked': 0}
    #         )
    #         work_time.hours_worked += session_duration
    #         work_time.save()
    #
    #         # Удалить `login_time` из сессии
    #         request.session.pop('login_time', None)

    # def track_work_time(self, request):
    #     if 'login_time' in request.session:
    #         login_time = request.session['login_time']
    #         if is_naive(login_time):
    #             login_time = make_aware(login_time)
    #
    #         logout_time = now()
    #
    #         session_duration = (logout_time - login_time).total_seconds() / 3600.0
    #         session_duration = Decimal(session_duration).quantize(Decimal('0.01'))
    #
    #         logger.info(f"Tracking work time for user {request.user.username}: {session_duration} hours.")
    #
    #         # Update work time
    #         work_time, created = WorkTime.objects.get_or_create(
    #             employee=request.user.employee,
    #             date=now().date(),
    #             defaults={'hours_worked': 0}
    #         )
    #         work_time.hours_worked += session_duration
    #         work_time.save()
    #
    #     request.session.pop('login_time', None)

    # def track_work_time(self, request):
    #     if 'login_time' in request.session:
    #         login_time = request.session['login_time']
    #         logout_time = now()
    #
    #         session_duration = (logout_time - login_time).total_seconds() / 3600.0
    #         session_duration = Decimal(session_duration).quantize(Decimal('0.01'))
    #
    #         logger.info(f"Tracking work time for user {request.user.username}: {session_duration} hours.")
    #
    #         # Update work time
    #         work_time, created = WorkTime.objects.get_or_create(
    #             employee=request.user.employee,
    #             date=now().date(),
    #             # defaults={'hours_worked': 0}
    #         )
    #         work_time.hours_worked += session_duration
    #         work_time.save()
    #
    #     request.session.pop('login_time', None)

#
# class WorkTimeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Логика обработки запроса
#         # if request.user.is_authenticated and not request.user.is_staff:
#         if request.user.is_authenticated:
#             # Сохраняем время начала сессии
#             if 'session_start_time' not in request.session:
#                 request.session['session_start_time'] = now().isoformat()
#
#         response = self.get_response(request)
#
#         # Логика обработки ответа
#         # if request.user.is_authenticated and not request.user.is_staff:
#         if request.user.is_authenticated:
#             session_start_time = request.session.get('session_start_time')
#             if session_start_time:
#                 start_time = datetime.datetime.fromisoformat(session_start_time)
#                 end_time = now()
#                 session_duration = Decimal((end_time - start_time).total_seconds() / 3600)  # Преобразуем в часы
#
#                 # Обновляем запись в WorkTime
#                 employee = request.user.employee
#                 work_time, created = WorkTime.objects.get_or_create(
#                     employee=employee,
#                     date=end_time.date(),
#                     defaults={'hours_worked': Decimal('0.00')}
#                 )
#                 work_time.hours_worked += session_duration
#                 work_time.save()
#
#                 # Удаляем из сессии время начала
#                 del request.session['session_start_time']
#
#         return response
