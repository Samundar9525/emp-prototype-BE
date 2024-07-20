from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class EmployeeLoginManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class EmployeeLogin(AbstractBaseUser):
    login_id = models.IntegerField(unique=True,primary_key=True)
    emp_no = models.IntegerField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = EmployeeLoginManager()

    USERNAME_FIELD = 'username'
    class Meta:
        db_table = 'employee_login'

    def __str__(self):
        return self.username
