# admin_management_app/admin.py
from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'action')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AuditLog)