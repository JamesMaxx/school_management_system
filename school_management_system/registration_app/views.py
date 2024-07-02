from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, StaffRegistrationForm, AdminRegistrationForm

def registration_view(request):
    return render(request, 'registration_app/registration.html', {})

def student_registration_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('registration_success')  # Replace 'registration_success' with your success URL name
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration_app/student_registration.html', {'form': form})

def staff_registration_view(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('registration_success')  # Replace 'registration_success' with your success URL name
    else:
        form = StaffRegistrationForm()
    return render(request, 'registration_app/staff_registration.html', {'form': form})

def admin_registration_view(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('registration_success')  # Replace 'registration_success' with your success URL name
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration_app/admin_registration.html', {'form': form})
