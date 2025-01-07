from django.urls import path
import main_app.views as v
from .views import *
from Pract import settings
from django.conf.urls.static import static as djstat

urlpatterns = [
    path('home/', v.home_page, name='home'),
    path('forbidden/', forbidden_view, name='forbidden'),
    path('export_csv/', export_data_csv, name='export_data_csv'),
    path('export_sql/', export_data_sql, name='export_data_sql'),
    path('login/', v.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reestr/', reestr_list, name='reestr_list'),
    path('reestr/<int:employee_id>/', employee_detail, name='reestr_detail'),
    path('deps/<int:dep_id>/', department_detail, name='deps_detail'),
    path('deps/', department_list, name='deps_list'),
    path('deps/<int:dep_id>/remove_employee/<int:employee_id>/confirm/', confirm_remove_employee,
                       name='confirm_remove_employee'),
    path('projects/', project_list, name='project_list'),
    path('projects/<int:project_id>/', project_detail, name='projects_detail'),
    path('tasks/', task_list, name='tasks_list'),
    path('tasks/edit/<int:task_id>/', task_edit_page, name='task_edit_page'),
    path('tasks_user/', user_tasks, name='user_task_page'),
    path('settings/', v.settings, name='settings_page'),

    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/add/', DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),

    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role_detail'),
    path('roles/add/', RoleCreateView.as_view(), name='role_add'),
    path('roles/<int:pk>/edit/', RoleUpdateView.as_view(), name='role_edit'),
    path('roles/<int:pk>/delete/', RoleDeleteView.as_view(), name='role_delete'),

    path('document_type/', DocumentTypeListView.as_view(), name='document_type_list'),
    path('document_type/<int:pk>/', DocumentTypetailView.as_view(), name='document_type_detail'),
    path('document_type/add/', DocumentTypeCreateView.as_view(), name='document_type_add'),
    path('document_type/<int:pk>/edit/', DocumentTypeUpdateView.as_view(), name='document_type_edit'),
    path('document_type/<int:pk>/delete/', DocumentTypeDeleteView.as_view(), name='document_type_delete'),

    path('document/', DocumentListView.as_view(), name='document_list'),
    path('document/<int:pk>/', DocumenttailView.as_view(), name='document_detail'),
    path('document/add/', DocumentCreateView.as_view(), name='document_add'),
    path('document/<int:pk>/edit/', DocumentUpdateView.as_view(), name='document_edit'),
    path('document/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),

    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/', EmployeeTypetailView.as_view(), name='employee_detail'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employee_reestr/add/', EmployeereestrCreateView.as_view(), name='employee_add_reestr'),
    path('employee/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),

    path('user/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/add/', UserCreateView.as_view(), name='user_add'),
    path('user/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    path('position/', PositionListView.as_view(), name='position_list'),
    path('position/<int:pk>/', PositionDetailView.as_view(), name='position_detail'),
    path('position/add/', PositionCreateView.as_view(), name='position_add'),
    path('position/<int:pk>/edit/', PositionUpdateView.as_view(), name='position_edit'),
    path('position/<int:pk>/delete/', PositionDeleteView.as_view(), name='position_delete'),

    path('emp_position/', EmployeePositionListView.as_view(), name='emp_position_list'),
    path('emp_position/<int:pk>/', EmployeePositionDetailView.as_view(), name='emp_position_detail'),
    path('emp_position/add/', EmployeePositionCreateView.as_view(), name='emp_position_add'),
    path('emp_position/<int:pk>/edit/', EmployeePositionUpdateView.as_view(), name='emp_position_edit'),
    path('emp_position/<int:pk>/delete/', EmployeePositionDeleteView.as_view(), name='emp_position_delete'),

    path('worktime/', WorkTimeListView.as_view(), name='work_time_list'),
    path('my-work-time/', user_work_time, name="user_work_time_page"),
    path('worktime/<int:pk>/', WorkTimeDetailView.as_view(), name='work_time_detail'),
    path('worktime/add/', WorkTimeCreateView.as_view(), name='work_time_add'),
    path('worktime/<int:pk>/edit/', WorkTimeUpdateView.as_view(), name='work_time_edit'),
    path('worktime/<int:pk>/delete/', WorkTimeDeleteView.as_view(), name='work_time_delete'),

    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/add/', ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/add/', TaskCreateView.as_view(), name='task_add'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    path('payroll/', PayrollListView.as_view(), name='payroll_list'),
    path('payroll/<int:pk>/', PayrollDetailView.as_view(), name='payroll_detail'),
    path('payroll/add/', PayrollCreateView.as_view(), name='payroll_add'),
    path('payroll/<int:pk>/edit/', PayrollUpdateView.as_view(), name='payroll_edit'),
    path('payroll/<int:pk>/delete/', PayrollDeleteView.as_view(), name='payroll_delete'),



] + djstat(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
