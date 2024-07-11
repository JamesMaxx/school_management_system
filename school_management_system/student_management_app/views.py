from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import Student


"""view student"""
def student_dashboard(request):
    return render(request, 'studestudent_dashboard.html')

""""

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')


@login_required
def student_profile(request):
    return render(request, 'student_profile.html')


@login_required
def student_attendance(request):
    return render(request, 'student_attendance.html')


@login_required
def student_marks(request):
    return render(request, 'student_marks.html')



@login_required
def student_fee(request):
    return render(request, 'student_fee.html')



@login_required
def student_result(request):
    return render(request, 'student_result.html')



@login_required
def student_login(request):
    return render(request, 'student_login.html')

def logout(request):
    return render(request, 'student_login.html')

"""

