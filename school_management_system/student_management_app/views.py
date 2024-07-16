from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentProfileForm
from .models import Student

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_management_app/student_list.html', {'students': students})

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_management_app/student_dashboard.html', {'student': student})

def login_links(request):
    return render(request, 'student_management_app/login_links.html')

@login_required
def home(request):
    return render(request, 'student_management_app/student_home.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if hasattr(user, 'student'):  # Check if the user is associated with a student profile
                student = get_object_or_404(Student, user=user)
                return redirect('student_management_app:student_dashboard', student_id=student.id)  # Redirect to student dashboard
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return redirect('student_management_app:login')
    else:
        return render(request, 'student_management_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('student_management_app:login')

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
            return redirect('student_management_app:student_profile', student_id=student.id)
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_management_app/update_student_profile.html', {'form': form, 'student': student})

@login_required
def delete_student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_management_app:home')
    return render(request, 'student_management_app/delete_student_profile.html', {'student': student})

@login_required
def complete_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_management_app:home')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_management_app/complete_profile.html', {'form': form, 'student': student})

@csrf_protect
def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            student = Student.objects.get(user=user)
            return redirect('student_management_app:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_management_app/student_registration.html', {'form': form})
