from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Staff, Qualification, Responsibility, Department
from django.contrib.auth.models import User
from .forms import StaffRegistrationForm, QualificationForm, ResponsibilityForm

def home(request):
    return render(request, 'staff_management_app/staff_home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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
        form = StaffProfileForm(request.POST, request.FILES, instance=staff.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff_id)
    else:
        form = StaffProfileForm(instance=staff.profile)
    return render(request, 'staff_management_app/update_staff_profile.html', {'form': form, 'staff': staff})

@login_required
def delete_staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.user.delete()
        staff.delete()
        messages.success(request, 'Staff profile deleted successfully')
        return redirect('staff_management_app:staff_home')
    return render(request, 'staff_management_app/delete_staff_profile.html', {'staff': staff})

def login_links(request):
    return render(request, 'staff_management_app/login_links.html')

def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff = Staff.objects.create(user=user, **form.cleaned_data)
            messages.success(request, 'Staff registered successfully')
            return redirect('staff_management_app:complete_profile', staff_id=staff.id)
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff_management_app/staff_registration.html', {'form': form})

@login_required
def complete_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        profile_form = StaffProfileForm(request.POST, request.FILES, instance=staff.profile)
        qualification_form = QualificationForm(request.POST, request.FILES)
        responsibility_form = ResponsibilityForm(request.POST)
        
        if profile_form.is_valid() and qualification_form.is_valid() and responsibility_form.is_valid():
            profile_form.save()
            qualification = qualification_form.save(commit=False)
            qualification.staff = staff
            qualification.save()
            responsibility = responsibility_form.save(commit=False)
            responsibility.staff = staff
            responsibility.save()
            messages.success(request, 'Profile completed successfully')
            return redirect('staff_management_app:staff_profile', staff_id=staff_id)
    else:
        profile_form = StaffProfileForm(instance=staff.profile)
        qualification_form = QualificationForm()
        responsibility_form = ResponsibilityForm()
    
    context = {
        'profile_form': profile_form,
        'qualification_form': qualification_form,
        'responsibility_form': responsibility_form,
        'staff': staff
    }
    return render(request, 'staff_management_app/complete_profile.html', context)
