from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register_student', views.student_registration_view, name='student-registration'),
    path('register_staff', views.staff_registration_view, name='staff-registration'),
    path('register_admin', views.admin_registration_view, name='admin-registration'),
    path('registration', views.registration_view, name = 'registration'),

]
