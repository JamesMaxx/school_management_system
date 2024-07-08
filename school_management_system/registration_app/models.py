from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model to determine the type of user
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='auth_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='auth_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

# Student Profile Registration
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=50)

    # Contact Information
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact1_name = models.CharField(max_length=50)
    emergency_contact1_phone = models.CharField(max_length=15)
    emergency_contact1_relationship = models.CharField(max_length=30)
    emergency_contact2_name = models.CharField(max_length=50)
    emergency_contact2_phone = models.CharField(max_length=15)
    emergency_contact2_relationship = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    # Academic Information
    admission_date = models.DateField()
    grade_level = models.CharField(max_length=10)
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True)

    # Health Information
    allergies = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    family_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    family_doctor_phone = models.CharField(max_length=15, blank=True, null=True)

    # Additional Information
    hobbies = models.TextField(blank=True, null=True)
    extra_curricular_activities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.first_name} {self.last_name} {self.student_id}'

# Staff Profile Registration
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    # Contact Information
    phone_number = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relationship = models.CharField(max_length=30)
    emergency_contact2_name = models.CharField(max_length=50)
    emergency_contact2_phone = models.CharField(max_length=15)
    emergency_contact2_relationship = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)

    # Professional Information
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    previous_employment = models.TextField(blank=True, null=True)

    # Additional Information
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    extra_curricular_involvement = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.first_name} {self.last_name} {self.staff_id}'

# Admin Profile Registration
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    # Contact Information
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact1_name = models.CharField(max_length=50)
    emergency_contact1_phone = models.CharField(max_length=15)
    emergency_contact1_relationship = models.CharField(max_length=30)
    emergency_contact2_name = models.CharField(max_length=50)
    emergency_contact2_phone = models.CharField(max_length=15)
    emergency_contact2_relationship = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='admin_photos/', blank=True, null=True)

    # Professional Information
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    admin_id = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    previous_employment = models.TextField(blank=True, null=True)

    # Additional Information
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.first_name} {self.last_name} {self.admin_id}'
