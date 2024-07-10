from django.db import models
from django.conf import settings
from registration_app.models import User  # Import your custom User model

class Venue(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField('Venue Name', max_length=100)
    address = models.CharField(max_length=300)
    phone = models.CharField('Phone Number', max_length=20, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self):
        return self.name

class Attendees(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Sport', 'Sport'),
        ('Cultural', 'Cultural'),
        ('Religious', 'Religious'),
        ('Academic', 'Academic'),
        ('Others', 'Others'),
    ]

    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Attendees, related_name='events_participated', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    apply_leave = models.BooleanField(default=False)

    def __str__(self):
        return self.title
