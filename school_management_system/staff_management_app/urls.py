from django.urls import path
from . import views

app_name = 'staff_management'

urlpatterns = [
    path('list/', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),
    # Add URLs for updating and deleting staff information
]
