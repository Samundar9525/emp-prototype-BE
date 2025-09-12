from django.db import models

class Department(models.Model):
    dept_no = models.CharField(max_length=4, primary_key=True)
    dept_name = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = 'department'

class Employee(models.Model):
    emp_no = models.AutoField(primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    hire_date = models.DateField()

    class Meta:
        db_table = 'employee'

class DeptEmp(models.Model):
    emp_no = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no')
    dept_no = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no')
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        db_table = 'dept_emp'
        unique_together = (('emp_no', 'dept_no'),)

class EmployeeDepartmentView(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    employee_name = models.CharField(max_length=255)
    department_id = models.CharField(max_length=4)
    department_name = models.CharField(max_length=40)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'employee_department_view'

class DepartmentEmployeeCounts(models.Model):
    dept_no = models.CharField(max_length=255, primary_key=True)
    dept_name = models.CharField(max_length=255)
    total_employees = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'department_employee_counts'



class Salary(models.Model):
    emp_no = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no', related_name='salaries')
    amount = models.IntegerField()
    from_date = models.DateField(primary_key=True)
    to_date = models.DateField()

    class Meta:
        db_table = 'salary'
        unique_together = (('emp_no', 'from_date'),)

    def __str__(self):
        return f'{self.emp_no} - {self.amount}'

    def __str__(self):
        return f'{self.emp_no} - {self.amount}'

class Title(models.Model):
    emp_no = models.OneToOneField(Employee, on_delete=models.CASCADE, db_column='emp_no', primary_key=True)
    title = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'title'

class SalaryHike(models.Model):
    emp_no = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no')
    from_date = models.DateField()
    current_salary = models.IntegerField()
    previous_salary = models.IntegerField()
    hike_percentage = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        managed = True
        db_table = 'salary_hike'
