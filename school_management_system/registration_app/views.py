from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, StudentRegistrationForm, StaffRegistrationForm, AdminRegistrationForm, CustomUserCreationForm

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('event_management:home')

def user_list_view(request):
    return render(request, 'registration_app/user_list.html', {
        'users': User.objects.all()
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'registration_app/user_list.html', {
                'users': User.objects.all()
            })
    else:
        form = AuthenticationForm()
    return render(request, 'registration_app/login.html', {'form': form})

def registration_view(request):
    return render(request, 'registration_app/registration.html', {})

def student_registration_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student account created successfully!')
            return redirect('registration_app:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration_app/student_registration.html', {'form': form})

def staff_registration_view(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff account created successfully!')
            return redirect('registration_app:login')
    else:
        form = StaffRegistrationForm()
    return render(request, 'registration_app/staff_registration.html', {'form': form})

def admin_registration_view(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created successfully!')
            return redirect('registration_app:login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration_app/admin_registration.html', {'form': form})
