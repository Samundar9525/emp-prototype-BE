from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("emp", views.get_emp_data, name="employee-data"),
    path("emp-exp", views.get_emp_exp, name="employee-exp"),
    path("emp-dept", views.get_employees_by_department, name="employee-department"),
    path("emp-dept-group", views.get_group_by_department, name="employee-department"),
    path("dept-dashboard", views.department_employee_counts_api, name="employee-department"),
    path('employees/<str:dept_no>/', views.employees_by_department, name='employees-by-department'),
    path('salary-hikes/<int:empid>', views.get_salary_hikes, name='salary-hikes'),
    path('employees-detail/<int:emp_no>/', views.get_employee_detail, name='employee-detail'),
    path('employee-current-department/<int:emp_no>/', views.get_employee_department, name='employee-current-department'),
    path('designation-timeline/<int:emp_no>/', views.get_designation_timeline, name='employee-current-department'),
]
