from django.db import models
from django.conf import settings

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    # Add any other relevant fields

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
