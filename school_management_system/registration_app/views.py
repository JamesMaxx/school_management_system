from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, StaffRegistrationForm, AdminRegistrationForm
from .models import User


def logout_user(request):
    """View for user logout."""
    logout(request)
    return redirect('event_management:landing_page')


@csrf_protect
def login_user(request):
    """View for user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('registration_app:user_list')  # Redirect to user list
    else:
        form = AuthenticationForm()
    return render(request, 'registration_app/login.html', {'form': form})


@login_required
def user_list_view(request):
    """View to display list of users."""
    users = User.objects.all()
    return render(request, 'registration_app/user_list.html', {'users': users})


def registration_view(request):
    """Base view for user registration."""
    return render(request, 'registration_app/registration.html')


def student_registration_view(request):
    """View for student registration."""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_app:login')  # Redirect to login page
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration_app/student_registration.html', {'form': form})


def staff_registration_view(request):
    """View for staff registration."""
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_app:login')  # Redirect to login page
    else:
        form = StaffRegistrationForm()
    return render(request, 'registration_app/staff_registration.html', {'form': form})


def admin_registration_view(request):
    """View for admin registration."""
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_app:login')  # Redirect to login page
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration_app/admin_registration.html', {'form': form})
