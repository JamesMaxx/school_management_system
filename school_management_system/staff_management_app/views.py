from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Staff
from .forms import StaffRegistrationForm

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
        form = StaffRegistrationForm(request.POST, instance=staff.user)
        if form.is_valid():
            user = form.save()
            staff.first_name = form.cleaned_data['first_name']
            staff.last_name = form.cleaned_data['last_name']
            staff.phone_number = form.cleaned_data['phone_number']
            staff.address = form.cleaned_data['address']
            staff.date_of_birth = form.cleaned_data['date_of_birth']
            staff.department = form.cleaned_data['department']
            staff.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff_id)
    else:
        form = StaffRegistrationForm(instance=staff.user)
    return render(request, 'staff_management_app/update_staff_profile.html', {'form': form, 'staff': staff})

@login_required
def delete_staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.user.delete()
        messages.success(request, 'Staff profile deleted successfully')
        return redirect('staff_management_app:home')
    return render(request, 'staff_management_app/delete_staff_profile.html', {'staff': staff})

def login_links(request):
    return render(request, 'staff_management_app/login_links.html')

@login_required
def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff = Staff.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                department=form.cleaned_data['department'],
                role='staff'  # Assuming a default value for role
            )
            messages.success(request, 'Staff registered successfully')
            return redirect('staff_management_app:complete_profile', staff_id=staff.id)
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff_management_app/staff_registration.html', {'form': form})

@login_required
def complete_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        profile_form = StaffRegistrationForm(request.POST, instance=staff.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff_id)
    else:
        profile_form = StaffRegistrationForm(instance=staff.user)
    
    context = {
        'profile_form': profile_form,
        'staff': staff
    }
    return render(request, 'staff_management_app/complete_profile.html', context)
