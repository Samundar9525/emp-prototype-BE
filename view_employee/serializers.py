from datetime import date
from rest_framework import serializers
from .models import Department, DepartmentEmployeeCounts, Employee, Salary, SalaryHike, Title

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['emp_no', 'first_name', 'last_name','gender','birth_date','hire_date']


class EmployeeExperienceSerializer(serializers.ModelSerializer):
    years_of_experience = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['emp_no', 'first_name', 'hire_date', 'years_of_experience']

    def get_years_of_experience(self, obj):
        current_date = date.today()
        return current_date.year - obj.hire_date.year - ((current_date.month, current_date.day) < (obj.hire_date.month, obj.hire_date.day))


class EmployeeDepartmentViewSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    department_id = serializers.CharField()
    department_name = serializers.CharField()


class DepartmentEmployeeCountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentEmployeeCounts
        fields = ['dept_no', 'dept_name', 'total_employees']


class SalaryHikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryHike
        fields = ['emp_no', 'from_date', 'current_salary', 'previous_salary', 'hike_percentage']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['dept_no', 'dept_name']

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ['amount']  # Only including current salary

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['title']  # Only including the title


class EmployeeDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Employee
        fields = ['emp_no', 'birth_date', 'first_name', 'last_name', 'gender', 'hire_date', 'department']
