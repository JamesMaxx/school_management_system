from django.contrib import admin
from .models import Staff
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'is_active']
    list_filter = ['is_active']
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
        ('Responsibilities and Qualifications', {
            'fields': ('responsibilities', 'qualifications'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['user']
