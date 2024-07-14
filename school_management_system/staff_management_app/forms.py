from django import forms
from .models import Staff, Qualification, Responsibility, StaffProfile

class StaffRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='staff')

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'role' :forms.ChoiceField(choices=[('student', 'Student')], widget=forms.Select(attrs={'class': 'form-control'}), initial='student')
        }




class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree', 'institution', 'year_completed']
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'year_completed': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 9999}),
        }

class ResponsibilityForm(forms.ModelForm):
    class Meta:
        model = Responsibility
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
