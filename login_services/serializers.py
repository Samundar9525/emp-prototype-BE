from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import EmployeeLogin, CustomUser

class EmployeeLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLogin
        fields = ['emp_no', 'username', 'password', 'created_at', 'last_login']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

    def create(self, validated_data):
        user = EmployeeLogin.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.name
        token['email'] = user.email
        return token
