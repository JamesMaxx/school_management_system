from django.contrib.auth.models import Group
from .models import StudentProfile, StaffProfile, AdminProfile

def create_user_with_profile(user, user_type, profile_data):
    user.save()

    if user_type == 'student':
        student_group, _ = Group.objects.get_or_create(name='Student')
        student_group.user_set.add(user)
        StudentProfile.objects.create(user=user, **profile_data)
    elif user_type == 'staff':
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        staff_group.user_set.add(user)
        StaffProfile.objects.create(user=user, **profile_data)
    elif user_type == 'admin':
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_group.user_set.add(user)
        AdminProfile.objects.create(user=user, **profile_data)

    return user
