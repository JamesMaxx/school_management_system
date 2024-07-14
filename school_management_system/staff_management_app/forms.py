from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Staff, Department, Qualification, Responsibility

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class StaffRegistrationForm(forms.ModelForm):
    DEPARTMENT_CHOICES = [
        ('English Department', 'English Department'),
        ('Mathematics Department', 'Mathematics Department'),
        ('Science Department', 'Science Department'),
        ('Social Studies Department', 'Social Studies Department'),
        ('Foreign Languages Department', 'Foreign Languages Department'),
        ('Physical Education Department', 'Physical Education Department'),
        ('Arts Department', 'Arts Department'),
        ('Administration', 'Administration'),
        ('Special Education Department', 'Special Education Department'),
        ('Counseling Department', 'Counseling Department'),
    ]

    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=True, initial='English Department')

    # Define choices for the role field
    ROLE_CHOICES = [('staff', 'Staff')]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), initial='staff', disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = 'staff'  # Set default role here
        self.fields['role'].disabled = True   # Disable the role field so only 'staff' is displayed

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'department', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['staff', 'degree', 'institution', 'year_completed', 'upload_certificate']
        widgets = {
            'staff': forms.HiddenInput(),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'year_completed': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 9999}),
            'upload_certificate': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ResponsibilityForm(forms.ModelForm):
    class Meta:
        model = Responsibility
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class StaffSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name or email'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments", widget=forms.Select(attrs={'class': 'form-control'}))
