from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from .models import User, StudentProfile, StaffProfile, AdminProfile

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Username format: first_name + last_name + _role_id (e.g., JohnDoe_stu1234 for students)."
        self.fields['password1'].help_text = "Your password must contain at least 8 characters and should not be too common."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."

class UserRegistrationForm(CustomUserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1, self.instance)
        except ValidationError as error:
            self.add_error('password1', error)
        return password1

class StudentRegistrationForm(UserRegistrationForm):
    student_id = forms.CharField(max_length=20, required=True, help_text="Student IDs should start with 'stu' followed by a four-digit number, e.g., stu1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}))
    admission_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    # Added help text to indicate the username format for students
    username = forms.CharField(max_length=150, required=True, help_text="Username format: first_name + last_name + _student_id", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['student_id', 'admission_date']
        labels = {
            'admission_date': 'Admission Date',
            'student_id': 'Student ID',
        }
        widgets = {
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}_{self.cleaned_data['student_id']}"

        if commit:
            user.save()
            student_group, _ = Group.objects.get_or_create(name='Student')
            student_group.user_set.add(user)
            StudentProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                student_id=self.cleaned_data['student_id'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                admission_date=self.cleaned_data['admission_date']
            )
        return user

class StaffRegistrationForm(UserRegistrationForm):
    staff_id = forms.CharField(max_length=20, required=True, help_text="Staff IDs should start with 'sta' followed by a four-digit number, e.g., sta1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}))
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    # Added help text to indicate the username format for staff
    username = forms.CharField(max_length=150, required=True, help_text="Username format: first_name + last_name + _staff_id", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['staff_id', 'hire_date']
        labels = {
            'hire_date': 'Hire Date',
            'staff_id': 'Staff ID',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'staff_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}_{self.cleaned_data['staff_id']}"

        if commit:
            user.save()
            staff_group, _ = Group.objects.get_or_create(name='Staff')
            staff_group.user_set.add(user)
            StaffProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                staff_id=self.cleaned_data['staff_id'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date']
            )
        return user

class AdminRegistrationForm(UserRegistrationForm):
    admin_id = forms.CharField(max_length=20, required=True, help_text="Admin IDs should start with 'admin' followed by a four-digit number, e.g., admin1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin ID'}))
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    # Added help text to indicate the username format for admins
    username = forms.CharField(max_length=150, required=True, help_text="Username format: first_name + last_name + _admin_id", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['admin_id', 'hire_date']
        labels = {
            'hire_date': 'Hire Date',
            'admin_id': 'Admin ID',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'admin_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin ID'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}_{self.cleaned_data['admin_id']}"

        if commit:
            user.save()
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            admin_group.user_set.add(user)
            AdminProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                admin_id=self.cleaned_data['admin_id']
            )
        return user
