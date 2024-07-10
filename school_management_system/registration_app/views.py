from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, StaffRegistrationForm, AdminRegistrationForm, CustomUserCreationForm
from .models import User
from .forms import CustomUserCreationForm

@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Assuming you are using password1 field for login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or wherever needed
                return redirect('registration_app:user_list')
            else:
                # Handle invalid login attempt
                # For example, add error message to the form
                form.add_error(None, _('Invalid username or password'))
    else:
        form = CustomUserCreationForm()

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
