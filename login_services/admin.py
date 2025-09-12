from django.contrib import admin
from .models import EmployeeLogin

@admin.register(EmployeeLogin)
class EmployeeLoginAdmin(admin.ModelAdmin):
    list_display = ('login_id', 'username', 'emp_no', 'is_staff', 'is_superuser', 'last_login', 'created_at')
    search_fields = ('username', 'emp_no')
    ordering = ('login_id',)
    
    # Customize the fieldsets for add/edit forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('emp_no',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )

    readonly_fields = ('created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('password',)
        return self.readonly_fields
