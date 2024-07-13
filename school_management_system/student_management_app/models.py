""" Models for the student_management_app app. """
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Student(models.Model):
    """
    Model to store information about students.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    admission_number = models.CharField(max_length=20, unique=True)
    date_admitted = models.DateField()
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.user.username}- {self.admission_number}"

class Course(models.Model):
    """
    Model to represent courses offered.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    """
    Model to track student enrollments in courses.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.course.name}"

class Attendance(models.Model):
    """
    Model to record student attendance.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # 'Present', 'Absent', 'Late', etc.

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.date}"

class PerformanceRecord(models.Model):
    """
    Model to store student academic performance records.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.course.name}: {self.grade}"

class Assignment(models.Model):
    """
    Model to represent assignments given to students.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.course.name}"

class Submission(models.Model):
    """
    Model to store student submissions for assignments.
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    submission_file = models.FileField(upload_to='submissions/')

    def __str__(self):
        return f"{self.assignment.title} - {self.student.first_name} {self.student.last_name}"
