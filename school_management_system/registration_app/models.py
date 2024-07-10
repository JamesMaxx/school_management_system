from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom User Model with additional fields for user typeclass User(AbstractUser):
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

# Base Profile Model with common fields for all profiles
class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact1_name = models.CharField(max_length=50)
    emergency_contact1_phone = models.CharField(max_length=15)
    emergency_contact1_relationship = models.CharField(max_length=30)
    emergency_contact2_name = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact2_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact2_relationship = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    class Meta:
        abstract = True

# Student Profile Model
class StudentProfile(BaseProfile):
    admission_date = models.DateField()
    grade_level = models.CharField(max_length=10)
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    allergies = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    family_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    family_doctor_phone = models.CharField(max_length=15, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    extra_curricular_activities = models.TextField(blank=True, null=True)
    Groups = models.ManyToManyField(Group, related_name='students', blank=True)
    is_student = models.BooleanField(default=True)
    group = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return f'{self.user.username} - {self.first_name} {self.last_name} - {self.email} - {self.group}'

# Staff Profile Model
class StaffProfile(BaseProfile):
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    previous_employment = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    extra_curricular_involvement = models.TextField(blank=True, null=True)
    Groups = models.ManyToManyField(Group, related_name='staff', blank=True)
    is_staff = models.BooleanField(default=True)
    group = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return f'{self.user.username} {self.first_name} {self.last_name} {self.email} { self.group}'

# Admin Profile Model
class AdminProfile(BaseProfile):
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    admin_id = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    previous_employment = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    Group = models.ManyToManyField(Group, related_name='admin', blank=True)
    is_admin = models.BooleanField(default=True)
    group = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} {self.first_name} {self.last_name} {self.Group.name}{self.user.is_admin} {self.group}'

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
