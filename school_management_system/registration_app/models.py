# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

<<<<<<< HEAD
# Custom User Model with additional fields for user type
=======
# User Model to determine the type of user
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

<<<<<<< HEAD
# Base Profile Model with common fields for all profiles
class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
=======
# Student Profile Registration
class StudentProfile(models.Model):
    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=50)
<<<<<<< HEAD
=======

    # Contact Information
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact1_name = models.CharField(max_length=50)
    emergency_contact1_phone = models.CharField(max_length=15)
    emergency_contact1_relationship = models.CharField(max_length=30)
    emergency_contact2_name = models.CharField(max_length=50)
    emergency_contact2_phone = models.CharField(max_length=15)
    emergency_contact2_relationship = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

<<<<<<< HEAD
    class Meta:
        abstract = True

# Student Profile Model
class StudentProfile(BaseProfile):
=======
    # Academic Information
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    admission_date = models.DateField()
    grade_level = models.CharField(max_length=10)
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True)
<<<<<<< HEAD
=======

    # Health Information
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    allergies = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    family_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    family_doctor_phone = models.CharField(max_length=15, blank=True, null=True)
<<<<<<< HEAD
=======

    # Additional Information
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    hobbies = models.TextField(blank=True, null=True)
    extra_curricular_activities = models.TextField(blank=True, null=True)

    def __str__(self):
<<<<<<< HEAD
        return f'{self.user.username} - {self.first_name} {self.last_name} ({self.student_id})'

# Staff Profile Model
class StaffProfile(BaseProfile):
=======
        return f'{self.user.username} - {self.first_name} {self.last_name} {self.student_id}'

# Staff Profile Registration
class StaffProfile(models.Model):
    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
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
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    previous_employment = models.TextField(blank=True, null=True)
<<<<<<< HEAD
=======

    # Additional Information
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    extra_curricular_involvement = models.TextField(blank=True, null=True)

    def __str__(self):
<<<<<<< HEAD
        return f'{self.user.username} - {self.first_name} {self.last_name} ({self.staff_id})'

# Admin Profile Model
class AdminProfile(BaseProfile):
=======
        return f'{self.user.username} - {self.first_name} {self.last_name} {self.staff_id}'

# Admin Profile Registration
class AdminProfile(models.Model):

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
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
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    admin_id = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    previous_employment = models.TextField(blank=True, null=True)
<<<<<<< HEAD
=======

    # Additional Information
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)

    def __str__(self):
<<<<<<< HEAD
        return f'{self.user.username} - {self.first_name} {self.last_name} ({self.admin_id})'

# Function to setup default groups and permissions
@receiver(post_save, sender=User)
def setup_default_groups_and_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            student_group, _ = Group.objects.get_or_create(name='Students')
            instance.groups.add(student_group)
            # Assign permissions for students if needed
        elif instance.is_staff:
            staff_group, _ = Group.objects.get_or_create(name='Staff')
            instance.groups.add(staff_group)
            # Assign permissions for staff if needed
        elif instance.is_admin:
            admin_group, _ = Group.objects.get_or_create(name='Admins')
            instance.groups.add(admin_group)
            # Assign permissions for admins if needed
=======
        return f'{self.user.username} - {self.first_name} {self.last_name} {self.admin_id}'
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
