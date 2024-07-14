# staff_management/models.py
from django.contrib.auth.models import User
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='staff/profile_pics/', blank=True, null=True)
    responsibilities = models.ManyToManyField('Responsibility', blank=True, related_name='staff_members')
    qualifications = models.ManyToManyField('Qualification', blank=True, related_name='staff_members')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='staff_members')
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Qualification(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    year_completed = models.IntegerField(null=True, blank=True)
    upload_certificate = models.FileField(upload_to='staff/certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.staff.first_name} {self.staff.last_name}'s Qualification"

class Responsibility(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='responsibilities')

    def __str__(self):
        return self.title


class StaffProfile(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='staff/profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.staff.first_name} {self.staff.last_name}'s Profile"
