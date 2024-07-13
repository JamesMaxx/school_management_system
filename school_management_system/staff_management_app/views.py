"""
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Staff
from .forms import StaffForm

@login_required
def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff_management/staff_list.html', {'staff_members': staff_members})

@login_required
def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.user = request.user
            staff.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff_management/staff_create.html', {'form': form})

"""

# Add views for updating and deleting staff information
