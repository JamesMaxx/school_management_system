# staff_management_app/admin.py
from django.contrib import admin
from .models import Staff, Department
from .forms import StaffAdminForm

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'is_active']
    list_filter = ['is_active', 'role']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    filter_horizontal = ['departments', 'responsibilities', 'qualifications']
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'is_active')
        }),
        ('Departments and Roles', {
            'fields': ('departments', 'role'),
            'classes': ('collapse',)
        }),

    )
    readonly_fields = ['user']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
