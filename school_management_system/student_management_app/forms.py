from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Attendance, Assignment
from datetime import date
from .models import TimetableEntry
from event_management.models import Event

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'})
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Course"
    )
    role = forms.ChoiceField(
        choices=[('student', 'Student')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='student'
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            student = self.save_student(user)
            self.save_enrollment(student)
        return user

    def save_student(self, user):
        student = Student.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            admission_number=self.generate_admission_number(),
            date_admitted=date.today(),
            address="",
            guardian_name="",
            guardian_contact="",
            email=user.email,
            active=True,
            profile_picture=None,
        )
        return student

    def save_enrollment(self, student):
        course = self.cleaned_data['course']
        Enrollment.objects.create(
            student=student,
            course=course,
            date_enrolled=date.today(),
            is_active=True
        )

    def generate_admission_number(self):
        latest_student = Student.objects.order_by('-id').first()
        if not latest_student:
            return 'S001'
        admission_number = latest_student.admission_number
        new_admission_int = int(admission_number.split('S')[-1]) + 1
        new_admission_number = 'S' + str(new_admission_int).zfill(3)
        return new_admission_number

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'date_of_birth', 'gender', 'guardian_name', 'guardian_contact', 'email', 'address', 'profile_picture']

class UpdateStudentForm(forms.ModelForm):
    new_course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['guardian_name', 'guardian_contact', 'email', 'phone', 'course']
        widgets = {
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.course:
            self.fields['new_course'].initial = self.instance.course

    def save(self, commit=True):
        student = super().save(commit=False)
        new_course = self.cleaned_data.get('new_course')
        if new_course and new_course != student.course:
            student.course = new_course
            if commit:
                student.save()
        return student

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['course', 'status']  # Include 'course' field in the form
        widgets = {
            'status': forms.Select(choices=[
                ('Present', 'Present'),
                ('Absent', 'Absent'),
                ('Late', 'Late'),
            ], attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'})  # Widget for course field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()  # Queryset for 'course' field


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']


class TimetableEntryForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = TimetableEntry
        fields = ['day', 'start_time', 'end_time', 'subject', 'teacher', 'location', 'event']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }