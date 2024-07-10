<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User
from .user_helpers import create_user_with_profile

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, user_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_type = user_type
        id_help_text = ""

        if self.user_type == 'student':
            self.fields['student_id'] = forms.CharField(max_length=20, required=True, help_text="Student IDs should start with 'stu' followed by a four-digit number, e.g., stu1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}))
            id_help_text = "Student ID format: stu1234"
        elif self.user_type == 'staff':
            self.fields['staff_id'] = forms.CharField(max_length=20, required=True, help_text="Staff IDs should start with 'sta' followed by a four-digit number, e.g., sta1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}))
            id_help_text = "Staff ID format: sta1234"
        elif self.user_type == 'admin':
            self.fields['admin_id'] = forms.CharField(max_length=20, required=True, help_text="Admin IDs should start with 'admin' followed by a four-digit number, e.g., admin1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin ID'}))
            id_help_text = "Admin ID format: admin1234"

        # Insert id field after last_name and before email
        self.fields['id_field'] = forms.CharField(max_length=20, required=True, help_text=id_help_text, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': f'{self.user_type.title()} ID'}))

        # Adjust field order
        field_order = list(self.fields.keys())
        field_order.insert(field_order.index('last_name') + 1, 'id_field')
        field_order.remove('username')  # Remove to re-add later in the desired position
        self.fields = forms.OrderedDict((key, self.fields[key]) for key in field_order)

        # Update username help text
        self.fields['username'].help_text = f"Enter your username. Format: firstname-lastname/{self.user_type}_id"

        # Update password help text
        self.fields['password1'].help_text = "Your password must contain at least 8 characters and should not be too common."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."

    def save(self, commit=True):
        user = super().save(commit=False)

        profile_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'date_of_birth': self.cleaned_data['date_of_birth'],
            'gender': self.cleaned_data['gender'],
            f'{self.user_type}_id': self.cleaned_data['id_field']
        }

        if self.user_type == 'student':
            user.is_student = True
            user.username = f"{self.cleaned_data['first_name']}-{self.cleaned_data['last_name']}/stu{self.cleaned_data['id_field']}"
        elif self.user_type == 'staff':
            user.is_staff = True
            user.username = f"{self.cleaned_data['first_name']}-{self.cleaned_data['last_name']}/sta{self.cleaned_data['id_field']}"
        elif self.user_type == 'admin':
            user.is_admin = True
            user.username = f"{self.cleaned_data['first_name']}-{self.cleaned_data['last_name']}/admin{self.cleaned_data['id_field']}"

        if commit:
            user = create_user_with_profile(user, self.user_type, profile_data)

        return user

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    username = forms.CharField(max_length=150, required=True, help_text="Enter your username. Format: firstname-lastname/role_id", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
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

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['admission_date']
        labels = {
            'admission_date': 'Admission Date',
        }
        widgets = {
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def save(self, commit=True):
        return super().save(commit=commit)

class StaffRegistrationForm(UserRegistrationForm):
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['hire_date']
        labels = {
            'hire_date': 'Hire Date',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def save(self, commit=True):
        return super().save(commit=commit)

class AdminRegistrationForm(UserRegistrationForm):
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['hire_date']
        labels = {
            'hire_date': 'Hire Date',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def save(self, commit=True):
        return super().save(commit=commit)
=======
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
        self.fields['username'].help_text = "Enter your username"
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


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
    admission_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    student_id = forms.CharField(max_length=20, required=True, help_text="Student IDs should start with 'stu' followed by a four-digit number, e.g., stu1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['admission_date', 'student_id']
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

        # Customize username format
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}_{self.cleaned_data['student_id']}"

        if commit:
            user.save()
            student_group, _ = Group.objects.get_or_create(name='Student')  # Ensure 'Student' group exists
            student_group.user_set.add(user)  # Assign user to 'Student' group

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
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    staff_id = forms.CharField(max_length=20, required=True, help_text="Staff IDs should start with 'sta' followed by a four-digit number, e.g., sta1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['hire_date', 'staff_id']
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

        # Customize username format
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}_{self.cleaned_data['staff_id']}"

        if commit:
            user.save()
            staff_group, _ = Group.objects.get_or_create(name='Staff')  # Ensure 'Staff' group exists
            staff_group.user_set.add(user)  # Assign user to 'Staff' group

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
    hire_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    admin_id = forms.CharField(max_length=20, required=True, help_text="Admin IDs should start with 'admin' followed by a four-digit number, e.g., admin1234.", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin ID'}))

    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields + ['hire_date', 'admin_id']
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

        # Customize username format
        user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['last_name']}_{self.cleaned_data['admin_id']}"

        if commit:
            user.save()
            admin_group, _ = Group.objects.get_or_create(name='Admin')  # Ensure 'Admin' group exists
            admin_group.user_set.add(user)  # Assign user to 'Admin' group

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
>>>>>>> 1fe54f53ec8cbf5fa848a6377cb6fed89a0f1768
