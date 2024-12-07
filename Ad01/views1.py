
from django.shortcuts import render, get_object_or_404
from .models import Event
from datetime import datetime

def calendar_view(request):
    days = range(1, 31)  # Days 1 to 31
    events = Event.objects.all()  # Retrieve all events from the database
    return render(request, 'calendar.html', {'days': days, 'events': events})


def event_details(request, date):
    # Dacă `date` reprezintă ziua din lună, o putem transforma într-un obiect datetime
    try:
        # Construieste data folosind ziua respectivă, luna și anul curent
        current_date = datetime.now()
        event_date = current_date.replace(day=int(date))  # Setează ziua respectivă

        # Caută evenimentul pentru acea dată
        event = Event.objects.get(date=event_date)

    except (ValueError, Event.DoesNotExist):
        event = None

    # Returnează template-ul cu informațiile despre eveniment (dacă există)
    return render(request, 'event_details.html', {'event': event})