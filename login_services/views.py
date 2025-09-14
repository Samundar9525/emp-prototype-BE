from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import CustomUser
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import json

@login_required
def index(request):
    return render(request, 'login_services/index.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'login_services/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'login_services/register.html')

        user = CustomUser.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'login_services/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            # Redirect to Angular app with token
            response = HttpResponse()
            response['Location'] = f'http://localhost:4200?token={str(refresh.access_token)}&username={user.name}'
            response.status_code = 302  # Redirect status code
            return response
        else:
            messages.error(request, 'Invalid email or password!')

    return render(request, 'login_services/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('username')
            password = data.get('password')
            print(email,password)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'status': 'success',
                    'username': user.name,
                    'email': user.email,
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'message': 'Login successful'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid credentials'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)