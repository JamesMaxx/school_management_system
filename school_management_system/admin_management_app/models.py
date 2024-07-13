# admin_management_app/models.py
from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
