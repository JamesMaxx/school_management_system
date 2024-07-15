# staff_management_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Staff, Department
from .forms import StaffRegistrationForm

@csrf_protect
def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the user object from the form
            user = form.save()

            # Create staff profile
            staff = form.save(commit=False)
            staff.user = user
            staff.save()

            # Set departments if provided
            departments = form.cleaned_data.get('departments')
            if departments:
                staff.departments.set(departments)

            # Success message and redirect
            messages.success(request, 'Staff registration successful')
            return redirect('staff_management_app:login')  # Replace with your desired redirect URL
        else:
            # Form validation errors
            messages.error(request, 'Please correct the errors below')
    else:
        form = StaffRegistrationForm()

    return render(request, 'staff_management_app/staff_registration.html', {'form': form})



def login_links(request):
    return render(request, 'staff_management_app/login_links.html')

@login_required
def home(request):
    return render(request, 'staff_management_app/staff_home.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'staff'):  # Check if the user is associated with a staff profile
                staff = get_object_or_404(Staff, user=user)
                return redirect('staff_management_app:staff_profile', staff_id=staff.id)  # Redirect to staff profile
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return redirect('staff_management_app:login')
    else:
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
        form = StaffProfileForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff.id)
    else:
        form = StaffProfileForm(instance=staff)
    return render(request, 'staff_management_app/update_staff_profile.html', {'form': form, 'staff': staff})

@login_required
def delete_staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff profile deleted successfully')
        return redirect('staff_management_app:home')
    return render(request, 'staff_management_app/delete_staff_profile.html', {'staff': staff})

@login_required
def complete_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff.id)
    else:
        form = StaffProfileForm(instance=staff)
    return render(request, 'staff_management_app/complete_profile.html', {'form': form, 'staff': staff})
