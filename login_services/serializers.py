from rest_framework import serializers
from .models import EmployeeLogin

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
