# staff_management_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Staff, Department
from .forms import StaffRegistrationForm

def login_links(request):
    return render(request, 'staff_management_app/login_links.html')

def home(request):
    return render(request, 'staff_management_app/staff_home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('staff_management_app:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'staff_management_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('staff_management_app:login')

@login_required
def staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'staff_management_app/staff_profile.html', {'staff': staff})

@login_required
def update_staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()  # Save the form data to update the staff profile
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff_id)
    else:
        form = StaffRegistrationForm(instance=staff)
    return render(request, 'staff_management_app/update_staff_profile.html', {'form': form, 'staff': staff})

@login_required
def delete_staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.delete()  # Delete the staff profile from the database
        messages.success(request, 'Staff profile deleted successfully')
        return redirect('staff_management_app:home')
    return render(request, 'staff_management_app/delete_staff_profile.html', {'staff': staff})

def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the new staff user to the database
            login(request, user)  # Log the user in
            return redirect('staff_management_app:home')
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff_management_app/staff_registration.html', {'form': form})

@login_required
def complete_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()  # Save the completed profile updates to the database
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff_id)
    else:
        form = StaffRegistrationForm(instance=staff)
    return render(request, 'staff_management_app/complete_profile.html', {'form': form, 'staff': staff})
