from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentProfileForm, CustomAuthenticationForm
from .models import Student

def login_links(request):
    return render(request, 'student_management_app/login_links.html')

def home(request):
    return render(request, 'student_management_app/student_home.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            student = get_object_or_404(Student, user=user)
            return redirect('student_management_app:student_profile', student_id=student.id)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'student_management_app/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('student_management_app:login')

@login_required
def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_management_app/student_profile.html', {'student': student})

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

@login_required
def delete_student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_management_app:home')
    return render(request, 'student_management_app/delete_student_profile.html', {'student': student})

def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account created for {username}. Please complete your profile details.')
            return redirect('student_management_app:complete_profile', student_id=student.id)
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_management_app/student_registration.html', {'form': form})

@login_required
def complete_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_management_app:login')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_management_app/complete_profile.html', {'form': form, 'student': student})
