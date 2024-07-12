from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, StudentProfileForm, CustomAuthenticationForm
from .models import Student

def home(request):
    return render(request, 'student_management_app/home.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            student = get_object_or_404(Student, user=user)
            return redirect('student_management:student_profile', student_id=student.id)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'student_management_app/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('student_management:login')

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
            return redirect('student_management:student_profile', student_id=student.id)
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_management_app/update_student_profile.html', {'form': form, 'student': student})

@login_required
def delete_student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_management:home')
    return render(request, 'student_management_app/delete_student_profile.html', {'student': student})
