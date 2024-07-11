from . models import Student
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'student_management'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),


]