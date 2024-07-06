
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepartmentEmployeeCounts, DeptEmp, Employee, EmployeeDepartmentView, SalaryHike
from .serializers import DepartmentEmployeeCountsSerializer, EmployeeDepartmentViewSerializer, EmployeeExperienceSerializer, EmployeeSerializer, SalaryHikeSerializer
from django.http import HttpResponse
from django.db import connection
from .models import DeptEmp, Employee, Salary, Title


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
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                emp_no,
                from_date,
                amount AS current_salary,
                COALESCE(LAG(amount) OVER (PARTITION BY emp_no ORDER BY from_date), 0) AS previous_salary,
                COALESCE(
                    ROUND(((amount - LAG(amount) OVER (PARTITION BY emp_no ORDER BY from_date))::decimal / LAG(amount) OVER (PARTITION BY emp_no ORDER BY from_date)) * 100, 1),
                    0
                ) AS hike_percentage
            FROM
                public.salary
            WHERE
                emp_no = %s
            ORDER BY
                emp_no,
                from_date
        """, [empid])
        rows = cursor.fetchall()

    salary_hikes = [
        SalaryHike(
            emp_no=row[0],
            from_date=row[1],
            current_salary=row[2],
            previous_salary=row[3],
            hike_percentage=row[4]
        ) for row in rows
    ]

    serializer = SalaryHikeSerializer(salary_hikes, many=True)
    return Response(serializer.data)


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