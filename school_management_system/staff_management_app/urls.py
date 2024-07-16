""" urls.py  fir staff_management_app  """
from django.urls import path
from . import views

app_name = 'staff_management_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('staff_profile/<int:staff_id>/', views.staff_profile, name='staff_profile'),
    path('update_staff_profile/<int:staff_id>/', views.update_staff_profile, name='update_staff_profile'),
    path('delete_staff_profile/<int:staff_id>/', views.delete_staff_profile, name='delete_staff_profile'),
    path('login_links/', views.login_links, name='login_links'),
    path('staff_registration/', views.staff_registration, name='staff_registration'),
    path('complete_profile/<int:staff_id>/', views.complete_profile, name='complete_profile'),
    path('staff_dashboard/<int:staff_id>/', views.staff_dashboard, name='staff_dashboard'),

]
