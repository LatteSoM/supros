

# myapp/forms.py
from django import forms
from .models import Department, DocumentType, Position, Role, User, Employee, EmployeePosition, Document, Project, Task, \
    Payroll, WorkTime


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']


class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'department']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'employee']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'date_hired', 'status']


class EmployeePositionForm(forms.ModelForm):
    class Meta:
        model = EmployeePosition
        fields = ['employee', 'position', 'start_date', 'end_date']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['employee', 'document_type', 'document_number', 'issue_date', 'expiry_date']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'created_by']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status']


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'year', 'month', 'salary', 'bonuses', 'deductions', 'net_salary']


class WorkTimeForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['employee', 'date', 'hours_worked', 'description']


class DepartmentFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Поиск по названию",
        widget=forms.TextInput(attrs={'placeholder': 'Введите название отдела', 'class': 'form-control'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        label="Сортировать по",
        choices=[
            ('name', 'По алфавиту'),
            ('employee_count', 'По количеству сотрудников')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class RemoveEmployeeForm(forms.Form):
    confirm = forms.BooleanField(label="Я подтверждаю удаление сотрудника из отдела")


class TaskFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label="Поиск по названию",
        widget=forms.TextInput(attrs={'placeholder': 'Введите название задачи', 'class': 'form-control'})
    )
    employee_name = forms.CharField(
        required=False,
        label="Имя сотрудника",
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя сотрудника', 'class': 'form-control'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="Проект",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        label="Сортировать по",
        choices=[
            ('title', 'По алфавиту'),
            ('employee_count', 'По количеству человек'),
            ('date', 'По дате (Ближайшие)')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус задачи",
        choices=[
            ('', 'Все'),
            ('Выдана', 'Выдана'),
            ('В работе', 'В работе'),
            ('На проверке', 'На проверке'),
            ('Выполнена', 'Выполнена'),
            ('На доработке', 'На доработке')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )





