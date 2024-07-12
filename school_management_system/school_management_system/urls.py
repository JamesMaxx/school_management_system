# school_management_system/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include(('event_management.urls', 'event_management'), namespace='event_management')),
    path('staff/', include(('staff_management_app.urls', 'staff_management_app'), namespace='staff_management_app')),
    path('student/', include(('student_management_app.urls', 'student_management_app'), namespace='student_management_app')),
]

admin.site.site_header = "ABC Group of Schools"
admin.site.site_title = "ABC Group of Schools"
admin.site.index_title = "Welcome to ABC Group of Schools Admin Portal"
