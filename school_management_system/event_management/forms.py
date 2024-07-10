from django import forms
from django.forms import ModelForm
from .models import Venue, Event, Attendees

from django import forms
from django.forms import ModelForm
from .models import Venue, Event, Attendees

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'event_type', 'date', 'start_time', 'end_time', 'venue', 'organizer', 'attendees', 'apply_leave')

        labels = {
            'title': 'Event Title',
            'description': 'Event Description',
            'event_type': 'Event Type',
            'date': 'Event Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'venue': 'Event Venue',
            'organizer': 'Organizer',
            'apply_leave': 'Apply Leave',

        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the event name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the event description'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.Select(attrs={'class': 'form-select'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'apply_leave': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'phone', 'web', 'email_address')

        labels = {
            'name': '',
            'address': '',
            'phone': '',
            'web': '',
            'email_address': ''
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }
