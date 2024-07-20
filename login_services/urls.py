from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', views.LoginView.as_view(), name='login'),
    path('departments/<int:emp_no>/', views.get_departments_by_employee, name='get_departments_by_employee'),
]
