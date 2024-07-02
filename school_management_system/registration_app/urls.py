from django.urls import path
from . import views

urlpatterns = [
    path('register/student/', views.student_registration_view, name='student-registration'),
    path('register/staff/', views.staff_registration_view, name='staff-registration'),
    path('register/admin/', views.admin_registration_view, name='admin-registration'),
    # Add more paths as needed
]
