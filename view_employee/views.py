from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepartmentEmployeeCounts, DeptEmp, Employee, EmployeeDepartmentView, SalaryHike
from .serializers import DepartmentEmployeeCountsSerializer, EmployeeDepartmentViewSerializer, EmployeeExperienceSerializer, EmployeeSerializer, SalaryHikeSerializer
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .models import DeptEmp, Employee, Salary, Title
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, sam this is home")

@api_view(['GET'])
def get_emp_data(request):
    employees = Employee.objects.all()[:10]
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_emp_exp(request):
    employees = Employee.objects.all()[:100]
    serializer = EmployeeExperienceSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_employees_by_department(request):
    queryset = EmployeeDepartmentView.objects.all()[:10]
    serializer = EmployeeDepartmentViewSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_group_by_department(request):
    try:
        queryset = EmployeeDepartmentView.objects.all()
        grouped_data = {}
        for entry in queryset:
            department_name = entry.department_name
            employee_id = entry.employee_id
            employee_name = entry.employee_name
            employee_data = {
                'employee_id': employee_id,
                'employee_name': employee_name,
            }
            if department_name in grouped_data:
                grouped_data[department_name].append(employee_data)
            else:
                grouped_data[department_name] = [employee_data]
        return Response(grouped_data)

    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def department_employee_counts_api(request):
    try:
        queryset = DepartmentEmployeeCounts.objects.all()
        serializer = DepartmentEmployeeCountsSerializer(queryset, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def employees_by_department(request, dept_no):
    try:
        emp_ids = DeptEmp.objects.filter(dept_no=dept_no).values_list('emp_no', flat=True)
        employees = Employee.objects.filter(emp_no__in=emp_ids)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_salary_hikes(request, empid):
    try:
        # First check if employee exists
        if not Employee.objects.filter(emp_no=empid).exists():
            return Response({'error': 'Employee not found'}, status=404)

        with connection.cursor() as cursor:
            cursor.execute("""
                WITH salary_data AS (
                    SELECT
                        emp_no,
                        from_date,
                        amount as current_salary,
                        LAG(amount) OVER (ORDER BY from_date) as previous_salary,
                        EXTRACT(YEAR FROM from_date) as year
                    FROM salary
                    WHERE emp_no = %s
                    ORDER BY from_date
                )
                SELECT
                    emp_no,
                    from_date,
                    current_salary,
                    COALESCE(previous_salary, current_salary) as previous_salary,
                    CASE
                        WHEN previous_salary IS NOT NULL AND previous_salary != 0
                        THEN ROUND(((current_salary - previous_salary)::decimal / previous_salary * 100), 1)
                        ELSE 0
                    END as hike_percentage
                FROM salary_data;
            """, [empid])
            rows = cursor.fetchall()

        if not rows:
            return Response({'error': 'No salary records found'}, status=404)

        salary_hikes = []
        for row in rows:
            if row[2] is not None:  # Only include rows with valid salary data
                hike = {
                    'from_date': row[1].strftime('%Y-%m-%d'),
                    'current_salary': int(row[2]),
                    'hike_percentage': float(row[4] if row[4] is not None else 0)
                }
                salary_hikes.append(hike)
        
        print(f"Salary data: {salary_hikes}")  # Debug print
        return Response(salary_hikes)

    except Exception as e:
        print(f"Error in get_salary_hikes: {str(e)}")
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_employee_detail(request, emp_no):
    try:
        employee = Employee.objects.get(emp_no=emp_no)
        employee_serializer = EmployeeSerializer(employee).data
        current_salary = Salary.objects.filter(emp_no=employee.emp_no).order_by('-from_date').first()
        if current_salary:
            employee_serializer['current_salary'] = current_salary.amount
        else:
            employee_serializer['current_salary'] = None

        current_title = Title.objects.filter(emp_no=employee.emp_no).order_by('-from_date').first()
        if current_title:
            employee_serializer['current_title'] = current_title.title
        else:
            employee_serializer['current_title'] = None
        return Response(employee_serializer)
    
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=404)
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_employee_department(request, emp_no):
    try:
        employee_department = EmployeeDepartmentView.objects.filter(employee_id=emp_no).order_by('to_date').first()
        return Response({
            'employee_id': employee_department.employee_id,
            'employee_name': employee_department.employee_name,
            'department_id': employee_department.department_id,
            'department_name': employee_department.department_name
        })
    except EmployeeDepartmentView.DoesNotExist:
        return Response({'error': 'Employee or department not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

def get_designation_timeline_data(emp_no):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT title, EXTRACT(YEAR FROM from_date) AS from_year, years
            FROM public.designation_timeline
            WHERE employee_id = %s
            ORDER BY from_date DESC
        """, [emp_no])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results

@api_view(['GET'])
def get_designation_timeline(request, emp_no):
    try:
        timeline_data = get_designation_timeline_data(emp_no)
        if not timeline_data:
            return Response({'error': 'Timeline not found'}, status=404)
        return Response(timeline_data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

class CreateEmployee(APIView):
    def post(self, request):
        emp_no = request.data.get('emp_no')
        birth_date = request.data.get('birth_date')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        gender = request.data.get('gender')
        hire_date = request.data.get('hire_date')

        employee = Employee(
            emp_no=emp_no,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            hire_date=hire_date
        )
        employee.save()

        return Response({'message': 'Employee Record Created Successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_next_emp_no(request):
    with connection.cursor() as cursor:
        cursor.execute("select emp_no from employee order by emp_no Desc limit 1")
        row = cursor.fetchone()
    return Response(row)

class UpdateEmployeeView(APIView):
    def put(self, request, emp_no):
        data = request.data
        employee = get_object_or_404(Employee, emp_no=emp_no)
        
        employee.birth_date = data.get('birth_date', employee.birth_date)
        employee.first_name = data.get('first_name', employee.first_name)
        employee.last_name = data.get('last_name', employee.last_name)
        employee.gender = data.get('gender', employee.gender)
        employee.hire_date = data.get('hire_date', employee.hire_date)
        
        employee.save()

        return JsonResponse({'message': 'Employee data updated Successfully'}, status=status.HTTP_200_OK)

class DeleteEmployeeView(APIView):
    def delete(self, request, emp_no):
        employee = get_object_or_404(Employee, emp_no=emp_no)
        employee.delete()
        return Response({'message': 'Employee deleted Successfully'}, status=status.HTTP_200_OK)