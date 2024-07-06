import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponse, HttpResponseRedirect
import csv

# Import PDF-related modules
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Paging-related modules
from django.core.paginator import Paginator


""" Generate pdf file venue list"""
def venue_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buf = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Set up the text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    # Add header
    textob.textLine("VENUES")
    textob.textLine("")

    # Fetch venues from the database
    venues = Venue.objects.all()

    # Add each venue's details
    for venue in venues:
        textob.textLine(f'Name: {venue.name}')
        textob.textLine(f'Address: {venue.address}')
        textob.textLine(f'Phone: {venue.phone}')
        textob.textLine(f'Website: {venue.web}')
        textob.textLine(f'Email: {venue.email_address}')
        textob.textLine("")  # Add a blank line for spacing

    # Draw the text on the PDF
    c.drawText(textob)
    c.showPage()
    c.save()

    # Move to the beginning of the StringIO buffer
    buf.seek(0)

    # Return the PDF response
    return FileResponse(buf, as_attachment=True, filename='venues.pdf')


""" Generate csv file venue list"""
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'

    # Create csv writer
    writer = csv.writer(response)

    # Designate the model
    venues = Venue.objects.all()

    # Add column headings to csv
    writer.writerow(['Name', 'Address', 'Phone', 'Website', 'Email'])


    # Loop through data and write to csv
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.web, venue.email_address])

    return response

""" Generate Text Files"""
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venues.txt"'

    # Designate the model
    venues = Venue.objects.all()

    lines = ["VENUES\n\n"]

    for venue in venues:
        lines.append(f'Name: {venue.name}\n')
        lines.append(f'Address: {venue.address}\n')
        lines.append(f'Phone: {venue.phone}\n')
        lines.append(f'Website: {venue.web}\n')
        lines.append(f'Email: {venue.email_address}\n\n')

    response.writelines(lines)
    return response

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('lists-venues')


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('lists-events')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events_management/update_event.html', {'event': event, 'form':form})

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events_management/add_event.html', {'form': form, 'submitted': submitted})



def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request, 'events_management/update_venue.html', {'venue': venue, 'form':form})

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        venues = Venue.objects.filter(name__contains=searched)


        return render(request, 'events_management/search_venues.html', {'searched':searched, 'venues':venues})
    else:
        return render(request, 'events_management/search_venues.html', {})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events_management/show_venue.html', {'venue': venue})


def list_venues(request):
    venue_list = Venue.objects.all()

    # Set Up Pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)

    return render(request, 'events_management/venue.html', {'venue_list': venue_list, 'venues': venues})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events_management/add_venue.html', {'form': form, 'submitted': submitted})

def all_events(request):
    event_list = Event.objects.all().order_by('date')
    venue_list = Venue.objects.all().order_by('name')
    return render(request, 'events_management/events_list.html', {'event_list': event_list, 'venue_list': venue_list})


def landingpage(request):
    return render(request, 'events_management/landingpage.html', {})

def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    first_name = "Elvis"
    second_name = "Mwanthi"
    month = month.capitalize()

    """ Convert month name to number """
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    """ Create a calendar """
    cal = HTMLCalendar().formatmonth(year, month_number, withyear=True)

    """ Get current year """
    now = datetime.now()
    current_year = now.year
    return render(request, 'events_management/home.html', {
        "first_name": first_name,
        "second_name": second_name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
    })
