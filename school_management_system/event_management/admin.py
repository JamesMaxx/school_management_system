from django.contrib import admin
from .models import Event, Venue, Attendees

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name', 'address')

@admin.register(Attendees)
class AttendeesAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone')
    search_fields = ('first_name', 'last_name', 'phone')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('title', 'venue'), 'date', ('start_time', 'end_time'), 'event_type', 'description', 'organizer', 'attendees')
    list_display = ('title', 'organizer', 'venue')
    list_filter = ('date', 'venue', 'organizer')
    search_fields = ('organizer__username', 'venue__name', 'title')

