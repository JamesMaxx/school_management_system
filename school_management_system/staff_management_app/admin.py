# staff_management_app/admin.py

from django.contrib import admin
from .models import Staff, Department, StaffLeave, PerformanceRecord, Assignment, Submission

admin.site.register(Staff)
admin.site.register(Department)
admin.site.register(StaffLeave)
admin.site.register(PerformanceRecord)
admin.site.register(Assignment)
admin.site.register(Submission)
