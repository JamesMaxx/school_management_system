# student_management_app/admin.py

from django.contrib import admin
from .models import Student, Course, Enrollment, Attendance, PerformanceRecord, Assignment, Submission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'phone', 'date_of_birth', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__first_name', 'user__last_name', 'admission_number')
    ordering = ('user__last_name', 'user__first_name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__name')
    ordering = ('-date_enrolled',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    list_filter = ('course', 'status')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__name')
    ordering = ('-date',)

@admin.register(PerformanceRecord)
class PerformanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade')
    list_filter = ('course', 'grade')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__name')
    ordering = ('student__user__last_name', 'student__user__first_name')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    list_filter = ('course',)
    search_fields = ('title', 'course__name')
    ordering = ('-due_date',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submission_date')
    list_filter = ('assignment__course',)
    search_fields = ('assignment__title', 'student__user__first_name', 'student__user__last_name')
    ordering = ('-submission_date',)

admin.site.site_header = "ABC Group of Schools"
admin.site.site_title = "ABC Group of Schools"
admin.site.index_title = "Welcome to ABC Group of Schools Admin Portal"
