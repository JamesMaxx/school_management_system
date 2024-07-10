<<<<<<< HEAD
from django.urls import path
from . import views

app_name = 'registration_app'  # This is your namespace

urlpatterns = [
    path('register/', views.registration_view, name='registration'),
    path('register/student/', views.student_registration_view, name='student_registration'),
    path('register/staff/', views.staff_registration_view, name='staff_registration'),
    path('register/admin/', views.admin_registration_view, name='admin_registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.user_list_view, name='user_list'),

]
=======
from django.urls import path
from . import views

app_name = 'registration_app'  # This is your namespace

urlpatterns = [
    path('register/', views.registration_view, name='registration'),
    path('register/student/', views.student_registration_view, name='student_registration'),
    path('register/staff/', views.staff_registration_view, name='staff_registration'),
    path('register/admin/', views.admin_registration_view, name='admin_registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.user_list_view, name='user_list'),

]
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
