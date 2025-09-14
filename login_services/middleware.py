from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require authentication for web interface
        exempt_urls = [
            reverse('login'),
            reverse('register'),
            '/admin/',
        ]

        # API endpoints - handle authentication differently
        if self._is_api_request(request):
            return self._handle_api_request(request)

        # Web interface authentication
        if not request.path_info in exempt_urls:
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('login')

        response = self.get_response(request)
        return response

    def _is_api_request(self, request):
        """Check if the request is for an API endpoint"""
        return (
            request.path_info.startswith('/api/') or
            request.path_info in ['/dept-dashboard', '/employees/', '/salary-hikes/', '/employees-detail/', '/employee-current-department/', '/designation-timeline/', '/create-employee/', '/update-employee/', '/delete-employee/', '/get-emp-no/'] or
            any(request.path_info.startswith(path) for path in ['/employees/', '/salary-hikes/', '/employees-detail/', '/employee-current-department/', '/designation-timeline/', '/create-employee/', '/update-employee/', '/delete-employee/'])
        )

    def _handle_api_request(self, request):
        """Handle API requests with proper authentication"""
        # For now, allow all API requests (implement proper auth later)
        # In production, you would check for JWT tokens, API keys, etc.
        response = self.get_response(request)

        # Add CORS headers for API responses
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response
