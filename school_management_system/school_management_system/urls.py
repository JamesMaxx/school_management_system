# school_management_system/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('event_management.urls')),
    path('', include('registration_app.urls')),  # Include registration_app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django auth URLs
    path('staff/', include('staff_management_app.urls')),
]



admin.site.site_header = "ABC Group of Schools"
admin.site.site_title = "ABC Group of Schools"
admin.site.index_title = "Welcome to ABC Group of Schools Admin Portal"