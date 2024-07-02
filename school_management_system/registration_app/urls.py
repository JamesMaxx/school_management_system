from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('registration', views.registration_view, name='registration'),
    path('student_registration', views.student_registration_view, name='student-registration'),
    path('staff_registration', views.staff_registration_view, name='staff-registration'),
    path('admin_registration', views.admin_registration_view, name='admin-registration'),
]
