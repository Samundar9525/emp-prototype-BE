from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.http import JsonResponse
from django.db import connection
from django.http import JsonResponse

def get_departments_by_employee(request, emp_no):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_departments_by_employee(%s)", [emp_no])
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return JsonResponse(results, safe=False)
def get_departments_by_employee(request, emp_no):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_departments_by_employee(%s)", [emp_no])
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return JsonResponse(results, safe=False)
User = get_user_model()

def index(request):
    return HttpResponse("Hello, sam this is login")

class LoginView(APIView): 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        if (password == user.password):
        # if check_password(password, user.password):
            user.last_login = timezone.now()
            user.save()
            return Response({"emp_no": user.emp_no, "username": user.username})
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)



def get_departments_by_employee(request, emp_no):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_departments_by_employee(%s)", [emp_no])
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return JsonResponse(results, safe=False)