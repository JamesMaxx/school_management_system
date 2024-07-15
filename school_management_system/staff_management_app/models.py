from django.db import models
from django.contrib.auth.models import User
from student_management_app.models import Course, Student  # Import models from student_management_app

# Define choices for roles
ROLE_CHOICES = [
    ('Teacher', 'Teacher'),
    ('Assistant Teacher', 'Assistant Teacher'),
    ('Administrator', 'Administrator'),
]

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    departments = models.ManyToManyField(Department)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StaffLeave(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"Leave application for {self.staff.first_name} {self.staff.last_name}"

class PerformanceRecord(models.Model):
    """
    Model to store student academic performance records.
    """
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('Fail', 'Fail'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performance_records_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='performance_records_course')
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.course.name}: {self.grade}"

class Assignment(models.Model):
    """
    Model to represent assignments given to students.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.course.name}"

class Submission(models.Model):
    """
    Model to store student submissions for assignments.
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    submission_file = models.FileField(upload_to='submissions/')

    def __str__(self):
        return f"{self.assignment.title} - {self.student.first_name} {self.student.last_name}"
