from django.db import models
from django.db.models import Count


# Отдел
class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название отдела")
    description = models.TextField(verbose_name="Описание отдела")

    @property
    def employee_count(self):
        return EmployeePosition.objects.filter(position__department=self).count()

    def __str__(self):
        return self.name


# Тип документа
class DocumentType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тип документа")

    def __str__(self):
        return self.name


# Должность
class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название должности")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")

    def __str__(self):
        return self.name


# Роль
class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name="Роль")

    def __str__(self):
        return self.name


# Сотрудник
class Employee(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField( verbose_name="Адрес эл.почты")
    date_hired = models.DateField(verbose_name="Дата приема на работу")
    experience = models.IntegerField(verbose_name="Стаж работы", default=0)
    status = models.CharField(max_length=50, choices=[
        ('Работает', 'Работает'),
        ('В отпуске', 'В отпуске'),
        ('Уволен', 'Уволен')
    ], verbose_name="Статус", default="Работает")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Пользователь
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, verbose_name="Роль")
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, verbose_name="Сотрудник")


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

        # Если пароль изменен, хешируем его

    # def save(self, *args, **kwargs):
    #     if self.pk is not None:  # Если это существующий объект
    #         orig = User.objects.get(pk=self.pk)
    #         if orig.password != self.password:  # Если пароль изменился
    #             self.set_password(self.password)  # Хешируем новый пароль
    #     else:
    #         self.set_password(self.password)  # Хешируем пароль при создании
    #
    #     super().save(*args, **kwargs)  # Вызываем метод родительского класса



# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.username





# Позиция сотрудника
class EmployeePosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Должность")
    start_date = models.DateField(verbose_name="Дата вступления в должность")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания действия назначения")


# Документ
class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name="Тип документа")
    document_number = models.CharField(max_length=255, verbose_name="Номер документа")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Действителен до")


# Проект
class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата конца")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Создан сотрудником")

    def __str__(self):
        return self.name


# Задача
class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', verbose_name="Назначена сотруднику")
    status = models.CharField(max_length=50, verbose_name="статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата саоздания")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата заверщения")

    def __str__(self):
        return self.title


from django.db import connection


# Расчет заработной платы
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    year = models.IntegerField(verbose_name="Год")
    month = models.IntegerField(verbose_name="Месяц")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Оклад")
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Надбавки")
    deductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Удержки")
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Чистая зарплата")

    def save(self, *args, **kwargs):
        # with connection.cursor() as cursor:
        #     self.net_salary = cursor.execute("SELECT calculate_net_salary(%s, %s, %s);", [self.salary, self.bonuses, self.deductions])
        #     result = cursor.fetchone()
        #     return result[0]
        self.net_salary = (self.salary or 0) + (self.bonuses or 0) - (self.deductions or 0)
        super().save(*args, **kwargs)


# Время работы
class WorkTime(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    date = models.DateField(verbose_name="Дата")
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Часов отработано")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
