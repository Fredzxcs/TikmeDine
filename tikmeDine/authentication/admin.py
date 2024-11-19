# your_app/admin.py
from django.contrib import admin
from .models import Employee  # Import the Employee model

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'job_title', 'account_status', 'role')  # Customize fields shown in the admin list view
    search_fields = ('username', 'email')  # Add search functionality
    list_filter = ('account_status', 'role')  # Add filters for better admin navigation

# Register Employee model with custom admin configuration
admin.site.register(Employee, EmployeeAdmin)
