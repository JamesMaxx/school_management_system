from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentProfileForm
from django.contrib.auth.forms import UserCreationForm
from .models import Student


def student_dashboard(request):
    return render(request, 'student_management_app/dashboard.html')




# Render the login links page
def login_links(request):
    return render(request, 'student_management_app/login_links.html')

# Render the home page for students
@login_required
def home(request):
    return render(request, 'student_management_app/student_home.html')


# Handle user login
"""
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            student = get_object_or_404(Student, user=user)
            return redirect('student_management_app:student_profile', student_id=student.id)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'student_management_app/login.html', {'form': form})
"""

# Handle user logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('student_management_app:login')

# Render the student profile page
@login_required
def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_management_app/student_profile.html', {'student': student})

# Update student profile
@login_required
def update_student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_management_app:student_profile', student_id=student.id)
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_management_app/update_student_profile.html', {'form': form, 'student': student})

# Delete student profile
@login_required
def delete_student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_management_app:home')
    return render(request, 'student_management_app/delete_student_profile.html', {'student': student})

# Complete student profile after registration
@login_required
def complete_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_management_app:home')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_management_app/complete_profile.html', {'form': form, 'student': student})



@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            student = get_object_or_404(Student, user=user)
            messages.success(request, f'Welcome, {user.username}. You have successfully logged in.')
            return redirect('student_management_app:student_profile', student_id=student.id)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('student_management_app:login')
    else:
        return render(request, 'student_management_app/login.html')


# Handle student registration
@csrf_protect
def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            student = Student.objects.get(user=user)
            return redirect('student_management_app:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_management_app/student_registration.html', {'form': form})