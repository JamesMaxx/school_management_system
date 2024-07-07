
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('event_management.urls')),
    path('', include('registration_app.urls')),

]

admin.site.site_header = "ABC Group of Schools"
admin.site.site_title = "ABC Group of Schools"
admin.site.index_title = "Welcome to ABC Group of Schools Admin Portal"