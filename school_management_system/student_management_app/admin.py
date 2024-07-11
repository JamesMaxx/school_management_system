from django.contrib import admin
from . models import Student

# Register your models here.
student_model = admin.site.register(Student)

admin.site.site_header = "ABC Group of Schools"
admin.site.site_title = "ABC Group of Schools"
admin.site.index_title = "Welcome to ABC Group of Schools Admin Portal"