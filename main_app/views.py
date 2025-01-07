# import os
#
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Count
from django.db.models.fields import return_None
from django.shortcuts import render, get_object_or_404


# from django.urls import reverse, reverse_lazy
# from django.http import HttpResponseRedirect, HttpResponse
# from django_filters.views import FilterView
# from openpyxl.workbook import Workbook
# from rest_framework import status, request
# from rest_framework.response import Response
#
#
# # import requests
#
#
# # Create your views here.
#
# #
# # def registration(request):
# #     a = 'adfghj'
# #     return render(request, 'main_app/index.html')
#
#
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# # from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
#
# from Pract import settings
# from api_app.models import *
# from .forms import UserRegistrationForm, UserLoginForm
# from .myfilters import BrandFilter, CatsFilter, ColorsFilter, SizesFilter, GoodsFilter, HugeCardFilter, MainCatsFilter, \
#     MainBrandsFilter, MainProductsFilter, SizeToGoodTableFilter, OrderFilter, OrderToGoodFilter
#
#
# def redirect_to_data(routing_name, **kwargs):
#     import requests
#     r = requests.post(f'http://localhost:8000/api/{routing_name}/', data=kwargs)
#     return r.text
#
#
# def register(request):
#     from api_app.models import Roles
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('login')
#             password = form.cleaned_data.get('password')
#             role = Roles.objects.get(name='user')
#             user = redirect_to_data('signup', login=username, password=password, role_id=role.id)
#             if user is not None:
#                 return redirect('login_page')  # Перенаправляем на страницу входа
#
#             return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'main_app/index.html', {'form': form})
#
#
# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('login')
#             password = form.cleaned_data.get('password')
#             user = redirect_to_data('login', login=username, password=password)
#             if 'token' in user:
#                 return redirect('home')  # Перенаправляем на домашнюю страницу
#     else:
#         form = UserLoginForm()
#     return render(request, 'main_app/login.html', {'form': form})
#
#
from django.utils import timezone
from django.utils.timezone import now

from .decorators import role_required
from .middleware import WorkTimeMiddleware, logger


def home_page(request):
    from main_app.models import Role, User, Employee  # Замените 'myapp' на имя вашего приложения

    # # Создание роли "admin"
    # admin_role, created = Role.objects.get_or_create(name='admin')
    #
    # # Создание сотрудника (можно указать реальные данные)
    # employee = Employee.objects.create(
    #     first_name='Admin',
    #     last_name='User',
    #     email='admin@example.com',
    #     date_hired='2023-01-01'  # Укажите дату, когда сотрудник был принят на работу
    # )
    #
    # # Создание пользователя с ролью "admin"
    # user = User.objects.create(
    #     username='admin',
    #     password='admin_password',  # Убедитесь, что вы используете хеширование паролей в реальном приложении
    #     role=admin_role,
    #     employee=employee
    # )
    # user = User.objects.get(username='evg')  # Замените 'admin' на имя пользователя, чей пароль вы хотите изменить
    #
    # #Установите новый пароль
    # new_password = 'agg'  # Укажите новый пароль
    # user.set_password(new_password)  # Хеширование пароля
    # user.save()  # Сохраните изменения

    user_role = request.user.role.name  # Получаем роль текущего пользователя

    if user_role == 'Администратор':
        return render(request, 'main_app/home.html')  # Главная для админа
    elif user_role == 'Педорг':
        return render(request, 'main_app/prj_list.html')  # Главная для менеджера
    elif user_role == 'Отдел Кадров':
        return render(request, 'main_app/reestr.html')  # Главная для сотрудника


    return render(request, 'main_app/home.html', {'user': request.user})

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Department, DocumentType, Position, Role, User, Employee, EmployeePosition, Document, Project, Task, \
    Payroll, WorkTime
from .forms import DepartmentForm, DocumentTypeForm, PositionForm, RoleForm, UserForm, EmployeeForm, \
    EmployeePositionForm, DocumentForm, ProjectForm, TaskForm, PayrollForm, WorkTimeForm, DepartmentFilterForm, \
    RemoveEmployeeForm, TaskFilterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def login_view(request):
    # Проверяем, пуста ли таблица пользователей
    if not User.objects.exists():
        # Создаём роль "admin", если её ещё нет
        admin_role, _ = Role.objects.get_or_create(name='Администратор')

        # Создаём сотрудника, связанного с администратором
        admin_employee = Employee.objects.create(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            date_hired=now().date(),
            experience=10,
            status='Работает'
        )

        # Создаём пользователя с ролью "admin"
        User.objects.create(
            username='admin',
            password=make_password('admin123'),  # Хэшируем пароль
            created_at=now(),
            role=admin_role,
            employee=admin_employee,
            is_superuser=True,
            # is_staff=True  # Добавляем атрибут is_staff для суперпользователя
        )

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['login_time'] = now().isoformat()  # Используем django.utils.timezone.now()
                request.session['user_role'] = user.role.name
                request.session['username'] = user.username
                logger.info(f"User {user.username} logged in at {request.session['login_time']}")
                return redirect('home')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(request, 'main_app/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logger.info(f"User {request.user.username} is logging out.")
        WorkTimeMiddleware(None).track_work_time(request)
        logout(request)

    return redirect('login')


import csv
import zipfile
from io import StringIO, BytesIO
from django.http import HttpResponse
from django.apps import apps
from django.db import connection


def export_data_csv(request):
    # Создаем буфер для архива
    zip_buffer = BytesIO()

    # Создание ZIP-архива
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Генерация CSV файлов
        for model in apps.get_models():
            model_name = model._meta.db_table
            file_name = f"{model_name}.csv"

            # Используем StringIO для генерации CSV в памяти
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            # Пишем заголовки
            fields = [field.name for field in model._meta.fields]
            writer.writerow(fields)

            # Пишем строки
            for obj in model.objects.all():
                writer.writerow([getattr(obj, field) for field in fields])

            # Добавляем CSV в ZIP
            zip_file.writestr(file_name, csv_buffer.getvalue().encode('utf-8'))

    # После выхода из блока `with` буфер `zip_buffer` готов к использованию
    zip_buffer.seek(0)  # Установить курсор на начало данных

    # Готовим ответ с ZIP-архивом
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="exported_data.zip"'
    return response


def export_data_sql(request):
    # Создаем буфер для архива
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:

        # 2. Генерация SQL скриптов
        with connection.cursor() as cursor:
            # Получаем список всех таблиц в базе данных
            for table_name in connection.introspection.table_names():
                file_name = f"{table_name}.sql"
                sql_buffer = StringIO()

                # Дамп структуры таблицы (если поддерживается)
                try:
                    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                    create_table_sql = cursor.fetchone()
                    if create_table_sql and create_table_sql[0]:
                        sql_buffer.write(f"{create_table_sql[0]};\n\n")
                except Exception as e:
                    sql_buffer.write(f"-- Ошибка при получении структуры таблицы {table_name}: {e}\n\n")

                # Дамп данных таблицы
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]

                    for row in rows:
                        values = ", ".join(
                            "'{}'".format(str(value).replace("'", "''")) if value is not None else "NULL"
                            for value in row
                        )
                        sql_buffer.write(
                            "INSERT INTO {} ({}) VALUES ({});\n".format(table_name, ", ".join(columns), values)
                        )

                except Exception as e:
                    sql_buffer.write(f"-- Ошибка при дампе данных таблицы {table_name}: {e}\n\n")

                # Добавляем SQL в ZIP
                zip_file.writestr(file_name, sql_buffer.getvalue().encode('utf-8'))

    # Готовим ответ с ZIP-архивом
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="exported_data.zip"'
    return response


def forbidden_view(request):
    return render(request, 'main_app/forbidden.html')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Payroll, Employee
import matplotlib

matplotlib.use('Agg')  # Устанавливаем backend для рендеринга графиков
import matplotlib.pyplot as plt
import io
import base64


def salary_trend(request, employee_id):
    # Получение данных сотрудника
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).order_by('year', 'month')

    # Подготовка данных для графика
    months = [f"{p.year}-{p.month:02d}" for p in payrolls]
    net_salaries = [p.net_salary for p in payrolls]
    salaries = [p.salary for p in payrolls]
    bonuses = [p.bonuses or 0 for p in payrolls]
    deductions = [p.deductions or 0 for p in payrolls]

    # Построение графика
    plt.figure(figsize=(12, 7))
    plt.plot(months, net_salaries, marker='o', label="Чистая зарплата", color="green", linewidth=2)
    plt.plot(months, salaries, marker='s', label="Оклад", color="blue", linestyle="--", linewidth=2)
    plt.plot(months, bonuses, marker='^', label="Бонусы", color="orange", linestyle=":", linewidth=2)
    plt.plot(months, deductions, marker='x', label="Взыскания", color="red", linestyle="-.")

    plt.title(f"Динамика зарплаты для  {employee.first_name} {employee.last_name}", fontsize=16)
    plt.xlabel("Дата (Год-месяц)", fontsize=12)
    plt.ylabel("Amount (Currency)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Конвертация графика в base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'main_app/salary_trend.html', {'employee': employee, 'graph': image_base64})


# Пример CRUD для Department
class DepartmentListView(ListView):
    model = Department
    template_name = 'main_app/department/department_list.html'
    context_object_name = 'departments'


class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'main_app/department/department_detail.html'
    context_object_name = 'department'


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'main_app/department/department_form.html'
    success_url = reverse_lazy('department_list')


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'main_app/department/department_form.html'
    success_url = reverse_lazy('department_list')


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'main_app/department/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')


class RoleListView(ListView):
    model = Role
    template_name = 'main_app/role/role_list.html'
    context_object_name = 'roles'


class RoleDetailView(DetailView):
    model = Role
    template_name = 'main_app/role/role_detail.html'
    context_object_name = 'role'


class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'main_app/role/role_form.html'
    success_url = reverse_lazy('role_list')


class RoleUpdateView(UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'main_app/role/role_form.html'
    success_url = reverse_lazy('role_list')


class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'main_app/role/role_confirm_delete.html'
    success_url = reverse_lazy('role_list')


class DocumentTypeListView(ListView):
    model = DocumentType
    template_name = 'main_app/document_type/document_type_list.html'
    context_object_name = 'document_type'


class DocumentTypetailView(DetailView):
    model = DocumentType
    template_name = 'main_app/document_type/document_type_detail.html'
    context_object_name = 'document_type'


class DocumentTypeCreateView(CreateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'main_app/document_type/document_type_form.html'
    success_url = reverse_lazy('document_type_list')


class DocumentTypeUpdateView(UpdateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'main_app/document_type/document_type_form.html'
    success_url = reverse_lazy('document_type_list')


class DocumentTypeDeleteView(DeleteView):
    model = DocumentType
    template_name = 'main_app/document_type/document_type_confirm_delete.html'
    success_url = reverse_lazy('document_type_list')


class EmployeeListView(ListView):
    model = Employee
    template_name = 'main_app/employee/employee_list.html'
    context_object_name = 'employee'


class EmployeeTypetailView(DetailView):
    model = Employee
    template_name = 'main_app/employee/employee_detail.html'
    context_object_name = 'employee'


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'main_app/employee/employee_form.html'
    success_url = reverse_lazy('employee_list')


class EmployeereestrCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'main_app/employee/employee_form.html'
    success_url = reverse_lazy('reestr_list')




class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'main_app/employee/employee_form.html'
    success_url = reverse_lazy('employee_list')


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'main_app/document_type/document_type_confirm_delete.html'
    success_url = reverse_lazy('employee_list')


class UserListView(ListView):
    model = User
    template_name = 'main_app/user/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'main_app/user/user_detail.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'main_app/user/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        # Получаем объект пользователя из формы
        user = form.save(commit=False)  # Не сохраняем еще в БД
        user.set_password(form.cleaned_data['password'])  # Хешируем пароль
        user.save()  # Теперь сохраняем пользователя с хешированным паролем
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'main_app/user/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        # Получаем объект пользователя из формы
        user = form.save(commit=False)  # Не сохраняем еще в БД
        user.set_password(form.cleaned_data['password'])  # Хешируем пароль
        user.save()  # Теперь сохраняем пользователя с хешированным паролем
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'main_app/user/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


class PositionListView(ListView):
    model = Position
    template_name = 'main_app/position/position_list.html'
    context_object_name = 'positions'


class PositionDetailView(DetailView):
    model = Position
    template_name = 'main_app/position/position_detail.html'
    context_object_name = 'positions'


class PositionCreateView(CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'main_app/position/position_form.html'
    success_url = reverse_lazy('position_list')


class PositionUpdateView(UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'main_app/position/position_form.html'
    success_url = reverse_lazy('position_list')


class PositionDeleteView(DeleteView):
    model = Position
    template_name = 'main_app/position/position_confirm_delete.html'
    success_url = reverse_lazy('position_list')


class EmployeePositionListView(ListView):
    model = EmployeePosition
    template_name = 'main_app/employee_position/emp_position_list.html'
    context_object_name = 'employees'


class EmployeePositionDetailView(DetailView):
    model = EmployeePosition
    template_name = 'main_app/employee_position/emp_position_detail.html'
    context_object_name = 'employee'


class EmployeePositionCreateView(CreateView):
    model = EmployeePosition
    form_class = EmployeePositionForm
    template_name = 'main_app/employee_position/emp_position_form.html'
    success_url = reverse_lazy('emp_position_list')


class EmployeePositionUpdateView(UpdateView):
    model = EmployeePosition
    form_class = EmployeePositionForm
    template_name = 'main_app/employee_position/emp_position_form.html'
    success_url = reverse_lazy('emp_position_list')


class EmployeePositionDeleteView(DeleteView):
    model = EmployeePosition
    template_name = 'main_app/employee_position/emp_position_confirm_delete.html'
    success_url = reverse_lazy('emp_position_list')


class DocumentListView(ListView):
    model = Document
    template_name = 'main_app/document/document_list.html'
    context_object_name = 'documents'


class DocumenttailView(DetailView):
    model = Document
    template_name = 'main_app/document/document_detail.html'
    context_object_name = 'document'


class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'main_app/document/document_form.html'
    success_url = reverse_lazy('document_list')


class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'main_app/document/document_form.html'
    success_url = reverse_lazy('document_list')


class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'main_app/document/document_confirm_delete.html'
    success_url = reverse_lazy('document_list')


class WorkTimeListView(ListView):
    model = WorkTime
    template_name = 'main_app/work_time/work_time_list.html'
    context_object_name = 'work_time'





class WorkTimeDetailView(DetailView):
    model = WorkTime
    template_name = 'main_app/work_time/work_time_detail.html'
    context_object_name = 'worktime'


class WorkTimeCreateView(CreateView):
    model = WorkTime
    form_class = WorkTimeForm
    template_name = 'main_app/work_time/work_time_form.html'
    success_url = reverse_lazy('work_time_list')


class WorkTimeUpdateView(UpdateView):
    model = Document
    form_class = WorkTimeForm
    template_name = 'main_app/work_time/work_time_form.html'
    success_url = reverse_lazy('work_time_list')


class WorkTimeDeleteView(DeleteView):
    model = WorkTime
    template_name = 'main_app/work_time/work_time_confirm_delete.html'
    success_url = reverse_lazy('work_time_list')


class ProjectListView(ListView):
    model = Project
    template_name = 'main_app/project/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'main_app/project/project_detail.html'
    context_object_name = 'project'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'main_app/project/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'main_app/project/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'main_app/project/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')


class TaskListView(ListView):
    model = Task
    template_name = 'main_app/task/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'main_app/task/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'main_app/task/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'main_app/task/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'main_app/task/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')


class PayrollListView(ListView):
    model = Payroll
    template_name = 'main_app/payroll/payroll_list.html'
    context_object_name = 'payrolls'


class PayrollDetailView(DetailView):
    model = Payroll
    template_name = 'main_app/payroll/payroll_detail.html'
    context_object_name = 'payroll'


class PayrollCreateView(CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'main_app/payroll/payroll_form.html'
    success_url = reverse_lazy('payroll_list')


class PayrollUpdateView(UpdateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'main_app/payroll/payroll_form.html'
    success_url = reverse_lazy('payroll_list')


class PayrollDeleteView(DeleteView):
    model = Payroll
    template_name = 'main_app/payroll/payroll_delete.html'
    success_url = reverse_lazy('payroll_list')

@role_required(['Отдел Кадров', 'Администратор'])
def reestr_list(request):
    # users = User.objects.all()
    # departments = Department.objects.all()
    # positions = Position.objects.all()
    #
    # # Фильтрация по отделам и должностям
    # department_filter = request.GET.get('department')
    # position_filter = request.GET.get('position')
    # search_query = request.GET.get('search')
    #
    # if department_filter:
    #     users = users.filter(employee__employeeposition__position__department__id=department_filter)
    # if position_filter:
    #     users = users.filter(employee__employeeposition__position__id=position_filter)
    # if search_query:
    #     users = users.filter(employee__first_name__icontains=search_query) | users.filter(employee__last_name__icontains=search_query)
    #
    # context = {
    #     'users': users,
    #     'departments': departments,
    #     'positions': positions,
    # }
    # return render(request, 'main_app/reestr.html', context)

    emps = Employee.objects.all()
    departments = Department.objects.all()
    positions = Position.objects.all()

    # Фильтрация по отделам и должностям
    department_filter = request.GET.get('department')
    position_filter = request.GET.get('position')
    search_query = request.GET.get('search')

    if department_filter:
        emps = emps.filter(employeeposition__position__department__id=department_filter)
    if position_filter:
        emps = emps.filter(employeeposition__position__id=position_filter)
    if search_query:
        emps = emps.filter(first_name__icontains=search_query) | emps.filter(
            last_name__icontains=search_query)

    context = {
        'employees': emps,
        'departments': departments,
        'positions': positions,
    }
    return render(request, 'main_app/reestr.html', context)

@role_required(['Отдел Кадров', 'Администратор'])
def employee_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    # Получаем связанные данные
    users = User.objects.filter(employee=employee)
    positions = EmployeePosition.objects.filter(employee=employee).select_related('position__department')
    payrolls = Payroll.objects.filter(employee=employee)
    documents = Document.objects.filter(employee=employee)
    tasks = Task.objects.filter(assigned_to=employee)

    # Получение данных сотрудника
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).order_by('year', 'month')

    # Подготовка данных для графика
    months = [f"{p.year}-{p.month:02d}" for p in payrolls]
    net_salaries = [p.net_salary for p in payrolls]
    salaries = [p.salary for p in payrolls]
    bonuses = [p.bonuses or 0 for p in payrolls]
    deductions = [p.deductions or 0 for p in payrolls]

    # Построение графика
    plt.figure(figsize=(10, 5))
    plt.plot(months, net_salaries, marker='o', label="Чистая зарплата", color="green", linewidth=2)
    plt.plot(months, salaries, marker='s', label="Оклад", color="blue", linestyle="--", linewidth=2)
    plt.plot(months, bonuses, marker='^', label="Бонусы", color="orange", linestyle=":", linewidth=2)
    plt.plot(months, deductions, marker='x', label="Взыскания", color="red", linestyle="-.")

    plt.title(f"Динамика зарплаты для  {employee.first_name} {employee.last_name}", fontsize=16)
    plt.xlabel("Дата (Год-месяц)", fontsize=12)
    plt.ylabel("Amount (Currency)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Конвертация графика в base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    context = {
        'employee': employee,
        'users': users,
        'positions': positions,
        'payrolls': payrolls,
        'documents': documents,
        'tasks': tasks,
        'graph': image_base64,
    }
    return render(request, 'main_app/reestr_detail.html', context)



def settings(request):
    return render(request, 'main_app/settings.html')

from django.http import JsonResponse, HttpResponseRedirect


@role_required(['Отдел Кадров', 'Администратор'])
def department_list(request):
    # departments = Department.objects.all()
    # form = DepartmentFilterForm(request.GET)
    # if form.is_valid():
    #     query = form.cleaned_data.get('query')
    #     sort_by = form.cleaned_data.get('sort_by')
    #     if query:
    #         departments = departments.filter(name__icontains=query)
    #     # Сортировка
    #     if sort_by == 'name':
    #         departments = departments.order_by('name')
    #     elif sort_by == 'employee_count':
    #         # departments = departments.order_by('-employee_count')
    #         departments = list(departments)
    #         departments.sort(key=lambda dept: dept.employee_count, reverse=True)
    #
    # return render(request, 'main_app/deps_list.html', {'departments': departments, 'form': form})


    # departments = Department.objects.all()
    # form = DepartmentFilterForm(request.GET)
    # form_add = DepartmentForm()
    #
    # # Проверка метода POST для добавления отдела
    # if request.method == 'POST' and request.is_ajax():
    #     form_add = DepartmentForm(request.POST)
    #     if form_add.is_valid():
    #         new_department = form_add.save()
    #         return JsonResponse({
    #             'success': True,
    #             'department': {
    #                 'id': new_department.id,
    #                 'name': new_department.position_set,
    #                 'employee_count': new_department.position_set.count()
    #             }
    #         })
    #     else:
    #         return JsonResponse({'success': False, 'errors': form_add.errors})
    #
    # # Фильтрация и сортировка
    # if form.is_valid():
    #     query = form.cleaned_data.get('query')
    #     sort_by = form.cleaned_data.get('sort_by')
    #
    #     if query:
    #         departments = departments.filter(name__icontains=query)
    #
    #     if sort_by == 'name':
    #         departments = departments.order_by('name')
    #     elif sort_by == 'employee_count':
    #         departments = sorted(departments, key=lambda dept: dept.position_set.count(), reverse=True)
    #
    # return render(request, 'main_app/deps_list.html', {'departments': departments, 'form': form, 'form_add': form_add})

    departments = Department.objects.all()
    form = DepartmentFilterForm(request.GET)
    form_add = DepartmentForm()

    # Обработка POST-запроса для добавления нового отдела
    if request.method == 'POST':
        form_add = DepartmentForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('deps_list')  # Перенаправление на ту же страницу после добавления отдела

    # Обработка GET-запроса с фильтрацией
    if form.is_valid():
        query = form.cleaned_data.get('query')
        sort_by = form.cleaned_data.get('sort_by')

        # Применение фильтрации и сортировки
        if query:
            departments = departments.filter(name__icontains=query)
        if sort_by == 'name':
            departments = departments.order_by('name')
        elif sort_by == 'employee_count':
            departments = sorted(departments, key=lambda dept: dept.employee_count, reverse=True)

    return render(request, 'main_app/deps_list.html', {
        'departments': departments,
        'form': form,
        'form_add': form_add  # Передача формы для модального окна
    })


@role_required(['Отдел Кадров'])
def department_detail(request, dep_id):

    department = get_object_or_404(Department, id=dep_id)
    sort_by = request.GET.get('sort_by', 'name')  # Default sorting by name
    search_query = request.GET.get('search_query')

    # Get employees in the department and apply sorting based on the chosen option
    employees = Employee.objects.filter(employeeposition__position__department=department)
    available_employees = Employee.objects.exclude(employeeposition__position__department=department)

    if search_query:
        available_employees = available_employees.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )

    # Sorting logic
    if sort_by == 'name':
        employees = employees.order_by('first_name', 'last_name')
    elif sort_by == 'position':
        employees = employees.order_by('employeeposition__position__name', 'first_name', 'last_name')

    if request.method == 'POST':
        # Handle adding an employee to the department
        employee_id = request.POST.get('employee_id')
        position = Position.objects.filter(department=department).first()  # Assuming one default position
        if employee_id and position:
            EmployeePosition.objects.create(
                employee_id=employee_id,
                position=position,
                start_date=timezone.now()
            )
            return redirect('deps_detail', dep_id=dep_id)


    return render(request, 'main_app/deps_detail.html', {
        'department': department,
        'employees': employees,
        'available_employees': available_employees,
        'search_query': search_query,
        'sort_by': sort_by,

    })


def remove_employee(request, dep_id, employee_id):
    department = get_object_or_404(Department, id=dep_id)
    EmployeePosition.objects.filter(employee_id=employee_id, position__department=department).delete()
    return redirect('deps_detail', dep_id=dep_id)


def confirm_remove_employee(request, dep_id, employee_id):
    department = get_object_or_404(Department, id=dep_id)
    employee_position = get_object_or_404(EmployeePosition, employee_id=employee_id, position__department=department)

    if request.method == 'POST':
        form = RemoveEmployeeForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            employee_position.delete()
            return redirect('deps_detail', dep_id=dep_id)
    else:
        form = RemoveEmployeeForm()

    return render(request, 'main_app/confirm_remove_employee.html', {
        'form': form,
        'department': department,
        'employee': employee_position.employee,
    })


def project_list(request):
    search_query = request.GET.get('search_query', '')
    sort_by = request.GET.get('sort', 'name')

    # Базовый запрос на получение проектов с аннотацией количества сотрудников и задач
    projects = Project.objects.annotate(
        employee_count=Count('task__assigned_to', distinct=True),
        task_count=Count('task')
    )

    # Фильтрация по названию
    if search_query:
        projects = projects.filter(name__icontains=search_query)

    # Сортировка
    if sort_by == 'name':
        projects = projects.order_by('name')
    elif sort_by == 'employee_count':
        projects = projects.order_by('-employee_count')
    elif sort_by == 'task_count':
        projects = projects.order_by('-task_count')

    return render(request, 'main_app/prj_list.html', {
        'projects': projects,
        'search_query': search_query,
        'sort_by': sort_by,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Список задач с сотрудниками, назначенными на выполнение
    tasks = Task.objects.filter(project=project).select_related('assigned_to')

    # Уникальный список сотрудников, задействованных в проекте
    # employees_in_project = EmployeePosition.objects.filter(
    #     employee__assigned_tasks__project=project
    # ).distinct()
    employees_in_project = Employee.objects.filter(
        assigned_tasks__project=project
    ).distinct()

    return render(request, 'main_app/prj_detail.html', {
        'project': project,
        'tasks': tasks,
        'employees_in_project': employees_in_project,
    })



def task_list(request):
    tasks = Task.objects.all().select_related('assigned_to', 'project')
    form = TaskFilterForm(request.GET)
    form_add = TaskForm()

    # Обработка POST-запроса для добавления новой задачи
    if request.method == 'POST':
        form_add = TaskForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('task_list')

    # Обработка GET-запроса с фильтрацией
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        project = form.cleaned_data.get('project')
        sort_by = form.cleaned_data.get('sort_by')
        status = form.cleaned_data.get('status')
        employee_name = form.cleaned_data.get('employee_name')

        # Фильтрация по названию задачи
        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        # Фильтрация по проекту
        if project:
            tasks = tasks.filter(project=project)

        # Фильтрация по статусу
        if status:
            tasks = tasks.filter(status=status)

        # Фильтрация по имени сотрудника
        if employee_name:
            tasks = tasks.filter(
                Q(assigned_to__first_name__icontains=employee_name) |
                Q(assigned_to__last_name__icontains=employee_name)
            )

        # Сортировка
        if sort_by == 'title':
            tasks = tasks.order_by('title')
        elif sort_by == 'employee_count':
            tasks = tasks.annotate(employee_count=Count('assigned_to')).order_by('-employee_count')
        elif sort_by == 'date':
            tasks = tasks.order_by('created_at')

    return render(request, 'main_app/tsk_list.html', {
        'tasks': tasks,
        'form': form,
        'form_add': form_add
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# @csrf_exempt
# def task_list(request):
#     tasks = Task.objects.all().select_related('assigned_to', 'project')
#     form = TaskFilterForm(request.GET)
#     form_add = TaskForm()
#
#     # Обработка POST-запроса для добавления новой задачи
#     if request.method == 'POST' and 'add-task-form' in request.POST:
#         form_add = TaskForm(request.POST)
#         if form_add.is_valid():
#             form_add.save()
#             return redirect('task_list')

    # # Обработка AJAX-запроса для редактирования задачи
    # if request.method == 'POST' and request.is_ajax():
    #     data = json.loads(request.body)
    #     task_id = data.get('id')
    #     title = data.get('title')
    #     description = data.get('description')
    #     status = data.get('status')
    #
    #     task = get_object_or_404(Task, id=task_id)
    #     task.title = title
    #     task.description = description
    #     task.status = status
    #     task.save()
    #
    #     return JsonResponse({'success': True})
    #
    # return render(request, 'main_app/tsk_list.html', {
    #     'tasks': tasks,
    #     'form': form,
    #     'form_add': form_add
    # })


def task_edit_page(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')  # Получаем статус из выпадающего списка
        task.save()
        return redirect('tasks_list')  # Перенаправление обратно на список задач после сохранения
    else:
        # Если метод GET, просто отобразите форму
        form = TaskForm(instance=task)

    return render(request, 'main_app/tsk_edit.html', {'form': form, 'task': task})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def user_tasks(request):
    # Проверяем, связан ли пользователь с сотрудником
    if not hasattr(request.user, 'employee') or not request.user.employee:
        # Если пользователь не связан с сотрудником, показываем сообщение
        return render(request, "main_app/error.html",
                      {"message": "Вы не связаны с сотрудником. Обратитесь к администратору."})

    # Получаем задачи текущего сотрудника
    tasks = Task.objects.filter(assigned_to=request.user.employee)

    if request.method == "POST":
        # Проходим по всем задачам из POST-запроса
        for task_id, new_status in request.POST.items():
            if task_id.startswith("task_"):  # Фильтруем ключи для задач
                task_id = task_id.replace("task_", "")  # Извлекаем ID задачи
                task = get_object_or_404(Task, id=task_id, assigned_to=request.user.employee)
                if new_status:  # Обновляем статус, если он передан
                    task.status = new_status
                    task.save()

        # Перенаправление на страницу задач после обновления
        return redirect("user_task_page")

    context = {"tasks": tasks}
    return render(request, "main_app/user_tasks.html", context)
# def user_tasks(request):
#     # Проверяем, связан ли пользователь с сотрудником
#     if not hasattr(request.user, 'employee') or not request.user.employee:
#         # Если пользователь не связан с сотрудником, показываем сообщение
#         return render(request, "main_app/error.html",
#                       {"message": "Вы не связаны с сотрудником. Обратитесь к администратору."})
#
#     # Получаем задачи текущего сотрудника
#     tasks = Task.objects.filter(assigned_to=request.user.employee)
#
#     if request.method == "POST":
#         # Получаем ID задачи и новый статус
#         task_id = request.POST.get("task_id")
#         new_status = request.POST.get("status")
#
#         # Ищем задачу, связанную с текущим сотрудником
#         task = get_object_or_404(Task, id=task_id, assigned_to=request.user.employee)
#
#         # Изменяем статус и сохраняем
#         if new_status:
#             task.status = new_status
#             task.save()
#
#         # Перенаправление на страницу задач
#         return redirect("user_task_page")
#
#     context = {"tasks": tasks}
#     return render(request, "main_app/user_tasks.html", context)
# def user_tasks(request):
#     # Получаем задачи текущего пользователя
#     tasks = Task.objects.filter(assigned_to=request.user)
#
#     if request.method == "POST":
#         # Обновление статуса задачи
#         task_id = request.POST.get("task_id")
#         new_status = request.POST.get("status")
#         task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
#
#         # Только изменение статуса
#         task.status = new_status
#         task.save()
#
#         # Перенаправление на ту же страницу после изменения
#         return redirect("user_tasks")
#
#     context = {"tasks": tasks}
#     return render(request, "main_app/user_tasks.html", context)


@login_required
def user_work_time(request):
    # Проверяем, связан ли пользователь с сотрудником
    if not hasattr(request.user, 'employee') or not request.user.employee:
        return render(request, "main_app/error.html",
                      {"message": "Вы не связаны с сотрудником. Обратитесь к администратору."})

    # Получаем рабочие часы текущего сотрудника
    work_times = WorkTime.objects.filter(employee=request.user.employee)

    context = {"work_times": work_times}
    return render(request, "main_app/user_work_time.html", context)
















