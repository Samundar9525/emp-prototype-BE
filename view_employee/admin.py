from django.contrib import admin
from .models import (
    Department, 
    Employee, 
    DeptEmp, 
    Salary, 
    Title, 
    EmployeeDepartmentView,
    DepartmentEmployeeCounts
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_no', 'dept_name')
    search_fields = ('dept_no', 'dept_name')
    ordering = ('dept_no',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date')
    search_fields = ('emp_no', 'first_name', 'last_name')
    list_filter = ('gender', 'hire_date')
    ordering = ('emp_no',)

@admin.register(DeptEmp)
class DeptEmpAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'dept_no', 'from_date', 'to_date')
    search_fields = ('emp_no__emp_no', 'dept_no__dept_no')
    list_filter = ('from_date', 'to_date')
    raw_id_fields = ('emp_no', 'dept_no')

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'amount', 'from_date', 'to_date')
    search_fields = ('emp_no__emp_no',)
    list_filter = ('from_date', 'to_date')
    raw_id_fields = ('emp_no',)

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'title', 'from_date', 'to_date')
    search_fields = ('emp_no__emp_no', 'title')
    list_filter = ('title', 'from_date', 'to_date')
    raw_id_fields = ('emp_no',)

@admin.register(EmployeeDepartmentView)
class EmployeeDepartmentViewAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_name', 'department_id', 'department_name', 'from_date', 'to_date')
    search_fields = ('employee_id', 'employee_name', 'department_name')
    list_filter = ('department_name',)

    def has_add_permission(self, request):
        return False  # Read-only view

    def has_change_permission(self, request, obj=None):
        return False  # Read-only view

    def has_delete_permission(self, request, obj=None):
        return False  # Read-only view

@admin.register(DepartmentEmployeeCounts)
class DepartmentEmployeeCountsAdmin(admin.ModelAdmin):
    list_display = ('dept_no', 'dept_name', 'total_employees')
    search_fields = ('dept_no', 'dept_name')

    def has_add_permission(self, request):
        return False  # Read-only view

    def has_change_permission(self, request, obj=None):
        return False  # Read-only view

    def has_delete_permission(self, request, obj=None):
        return False  # Read-only view


