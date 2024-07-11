""" registration_app views """
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, StaffRegistrationForm, AdminRegistrationForm, CustomUserLoginForm
from .models import User
from django.utils.translation import gettext_lazy as _


@csrf_protect
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


def user_list_view(request):
    users = User.objects.all()
    return render(request, 'registration_app/user_list.html', {'users': users})

def logout_view(request):
    logout(request)
    return redirect('event_management:landingpage')

def hello_view(request):
    return render(request, 'registration_app/hello.html')

@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('registration_app:dashboard')  # Redirect to user list page after login
            else:
                form.add_error(None, _('Invalid email or password'))
    else:
        form = CustomUserLoginForm()

    return render(request, 'registration_app/login.html', {'form': form})


def registration_view(request):
    return render(request, 'registration_app/registration.html')

def student_registration_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_app:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration_app/student_registration.html', {'form': form})

def staff_registration_view(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_app:login')
    else:
        form = StaffRegistrationForm()
    return render(request, 'registration_app/staff_registration.html', {'form': form})

def admin_registration_view(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_app:login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration_app/admin_registration.html', {'form': form})
