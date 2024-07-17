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
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'})
        }

class UpdateStudentForm(forms.ModelForm):
    new_course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['guardian_name', 'guardian_contact', 'email', 'phone', 'profile_picture']
        widgets = {
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student = kwargs.get('instance')
        if student:
            enrollment = Enrollment.objects.filter(student=student, is_active=True).first()
            if enrollment:
                self.fields['new_course'].initial = enrollment.course

    def save(self, commit=True):
        student = super().save(commit=False)
        new_course = self.cleaned_data['new_course']
        enrollment = Enrollment.objects.filter(student=student, is_active=True).first()
        if enrollment:
            enrollment.course = new_course
            enrollment.save()
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


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['pdf_file']

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data['pdf_file']
        # Ensure only PDF files are uploaded
        if not pdf_file.name.endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')
        return pdf_file

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'pdf_file', 'uploaded_by']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'uploaded_by': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),

        }