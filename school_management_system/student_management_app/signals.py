# signals.py in student_management_app

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Student

def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

post_save.connect(create_student_profile, sender=User)
