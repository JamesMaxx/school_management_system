from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from .models import User, StudentProfile, StaffProfile, AdminProfile

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    username = forms.CharField(max_length=150, help_text="Enter the username you received from administration via email.\nThe username format you're generating (first_name + last_name/user_type_id)", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
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
    admission_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    grade_level = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grade Level'}))
    student_id = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['admission_date', 'grade_level', 'student_id']
        labels = {
            'admission_date': 'Admission Date',
            'grade_level': 'Grade Level',
            'student_id': 'Student ID',
        }
        widgets = {
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grade Level'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True

        # Customize username format
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}/student_{self.cleaned_data['student_id']}"

        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                admission_date=self.cleaned_data['admission_date'],
                grade_level=self.cleaned_data['grade_level'],
                student_id=self.cleaned_data['student_id']
            )
        return user

class StaffRegistrationForm(UserRegistrationForm):
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    position = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}))
    department = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}))
    staff_id = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['hire_date', 'position', 'department', 'staff_id']
        labels = {
            'hire_date': 'Hire Date',
            'position': 'Position',
            'department': 'Department',
            'staff_id': 'Staff ID',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'staff_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True

        # Customize username format
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}/staff_{self.cleaned_data['staff_id']}"

        if commit:
            user.save()
            StaffProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                position=self.cleaned_data['position'],
                department=self.cleaned_data['department'],
                staff_id=self.cleaned_data['staff_id']
            )
        return user

class AdminRegistrationForm(UserRegistrationForm):
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    position = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}))
    department = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}))
    admin_id = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin ID'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['hire_date', 'position', 'department', 'admin_id']
        labels = {
            'hire_date': 'Hire Date',
            'position': 'Position',
            'department': 'Department',
            'admin_id': 'Admin ID',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'admin_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin ID'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True

        # Customize username format
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}/admin_{self.cleaned_data['admin_id']}"

        if commit:
            user.save()
            AdminProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                position=self.cleaned_data['position'],
                department=self.cleaned_data['department'],
                admin_id=self.cleaned_data['admin_id']
            )
        return user
