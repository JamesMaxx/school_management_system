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


class StaffForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

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
            'role' :forms.ChoiceField(choices=[('staff', 'Staff')], widget=forms.Select(attrs={'class': 'form-control'}), initial='staff')
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            self.save_staff(user)
        return user

    def save_staff(self, user):
        staff = Staff.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            address="",  # Add the actual address if available
            email=user.email,
            active=True,
            profile_picture=None  # Handle file upload if needed
        )
        return staff
