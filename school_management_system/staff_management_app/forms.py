from django import forms
from .models import Staff, Department, Qualification, Responsibility, StaffProfile

class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'is_active', 'profile_picture', 'department', 'role']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree', 'institution', 'year_completed', 'upload_certificate']
        widgets = {
            'year_completed': forms.NumberInput(attrs={'min': 1900, 'max': 9999}),
        }

class ResponsibilityForm(forms.ModelForm):
    class Meta:
        model = Responsibility
        fields = ['title', 'description']

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['profile_picture']

class StaffSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search by name or email'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments")
    is_active = forms.ChoiceField(choices=[('', 'All'), ('True', 'Active'), ('False', 'Inactive')], required=False)
