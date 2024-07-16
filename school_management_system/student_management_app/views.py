from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentProfileForm, AttendanceForm, AssignmentForm
from .models import Student, Attendance, Course, Assignment
from .utils import generate_weekday_dates
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse


def student_assignment_list(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    assignments = Assignment.objects.filter(uploaded_by=student)
    return render(request, 'student_management_app/student_assignment_list.html', {'assignments': assignments, 'student': student})

def student_upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.uploaded_by = request.user
            assignment.save()
            return redirect('student_management_app:student_assignment_list')  # Replace with the URL name for student's assignment list
    else:
        form = AssignmentForm()
    return render(request, 'student_management_app/student_upload_assignment.html', {'form': form})

def student_download_assignment(request, assignment_id):
    # Fetch the assignment object based on assignment_id
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Assuming you store the file in assignment.file_upload, you can serve it for download
    file_path = assignment.file_upload.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + assignment.file_upload.name
        return response
    raise Http404


def student_attendance_calendar(request):
    start_date = date.today()  # Start from today
    end_date = start_date + timedelta(days=1)  # Example: Show next 30 days

    weekday_dates = generate_weekday_dates(start_date, end_date)
    students = Student.objects.all()  # Get all students, adjust query as needed

    if request.method == 'POST':
        for student in students:
            for attendance_date in weekday_dates:
                form = AttendanceForm(request.POST)
                if form.is_valid():
                    attendance = form.save(commit=False)
                    attendance.student = student
                    attendance.date = attendance_date
                    attendance.save()

    context = {
        'weekday_dates': weekday_dates,
        'students': students,
    }
    return render(request, 'student_management_app/student_attendance_calendar.html', context)

def student_attendance_list(request):
    attendances = Attendance.objects.all()  # Fetch all attendance records
    context = {
        'attendances': attendances,
    }
    return render(request, 'student_management_app/student_attendance_list.html', context)

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
