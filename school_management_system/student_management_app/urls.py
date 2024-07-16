from django.urls import path
from . import views

app_name = 'student_management_app'

urlpatterns = [
    path('', views.home, name='student_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student_profile/<int:student_id>/', views.student_profile, name='student_profile'),
    path('update_student_profile/<int:student_id>/', views.update_student_profile, name='update_student_profile'),
    path('delete_student_profile/<int:student_id>/', views.delete_student_profile, name='delete_student_profile'),
    path('login_links/', views.login_links, name='login_links'),
    path('student_registration/', views.student_registration, name='student_registration'),
    path('complete_profile/<int:student_id>/', views.complete_profile, name='complete_profile'),
    path('student_dashboard/<int:student_id>', views.student_dashboard, name='student_dashboard'),
    path('student_list/', views.student_list, name='student_list'),
    path('student_attendance_calendar/', views.student_attendance_calendar, name='student_attendance_calendar'),
    path('student_attendance_list/', views.student_attendance_list, name='student_attendance_list'),
    path('student_upload_assignment/<int:student_id>/', views.student_upload_assignment, name='student_upload_assignment'),
    path('student_download_assignment/<int:assignment_id>/', views.student_download_assignment, name='student_download_assignment'),
    path('student_assignment_list/<int:student_id>/', views.student_assignment_list, name='student_assignment_list'),


]
