# Generated by Django 5.0.4 on 2024-11-22 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_employee_experience_employee_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_number',
            field=models.CharField(max_length=255, verbose_name='Номер документа'),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.documenttype', verbose_name='Тип документа'),
        ),
        migrations.AlterField(
            model_name='document',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='document',
            name='expiry_date',
            field=models.DateField(blank=True, null=True, verbose_name='Действителен до'),
        ),
        migrations.AlterField(
            model_name='document',
            name='issue_date',
            field=models.DateField(verbose_name='Дата выдачи'),
        ),
        migrations.AlterField(
            model_name='documenttype',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Тип документа'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_hired',
            field=models.DateField(verbose_name='Дата приема на работу'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Адрес эл.почты'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Отдел Фамилия'),
        ),
        migrations.AlterField(
            model_name='employeeposition',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='employeeposition',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания действия назначения'),
        ),
        migrations.AlterField(
            model_name='employeeposition',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.position', verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='employeeposition',
            name='start_date',
            field=models.DateField(verbose_name='Дата вступления в должность'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='bonuses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Надбавки'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='deductions',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Удержки'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='month',
            field=models.IntegerField(verbose_name='Месяц'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='net_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Чистая зарплата'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Оклад'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='year',
            field=models.IntegerField(verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='position',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.department', verbose_name='Отдел'),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название должности'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создан сотрудником'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(verbose_name='Дата конца'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to='main_app.employee', verbose_name='Назначена сотруднику'),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата заверщения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата саоздания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.project', verbose_name='Проект'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(max_length=50, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='user',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.role', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='hours_worked',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Часов отработано'),
        ),
    ]
