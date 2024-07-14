from django import forms
from django.contrib.auth.models import User
from .models import Staff

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

    ROLE_CHOICES = [
        ('staff', 'Staff'),
    ]
    # Fields from User model
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), required=True, initial='staff', label='Role', choices=ROLE_CHOICES)
    class Meta:
        model = User  # Using User model as base for registration
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'role']

class StaffAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Staff
        fields = '__all__'


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Staff.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                department=self.cleaned_data['department'],
                role=self.cleaned_data['role'],
            )
        return user
