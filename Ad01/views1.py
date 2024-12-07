
from django.shortcuts import render, get_object_or_404
from .models import Event
from .models import Program
from datetime import datetime
from django.contrib import messages

def calendar_view(request, month=None, year=None):
    # Obținem data curentă dacă nu se specifică luna și anul
    if not month or not year:
        current_date = datetime.now()
        month = current_date.month
        year = current_date.year
    else:
        month = int(month)
        year = int(year)

    # Obținem numele lunii
    month_name = datetime(year, month, 1).strftime('%B')

    # Obținem zilele lunii respective
    days_in_month = [day for day in range(1, 32)]
    # Verificăm validitatea zilelor
    valid_days = []
    for day in days_in_month:
        try:
            valid_days.append(datetime(year, month, day))
        except ValueError:
            break  # Dacă ziua nu există în luna respectivă, ieșim din buclă

    # Căutăm evenimentele pentru luna respectivă
    events = Program.objects.filter(start_time__month=month, start_time__year=year)

    return render(request, 'calendar.html', {
        'month_name': month_name,
        'events': events,
        'days': valid_days,
        'current_month': month,
        'current_year': year,
    })


def event_details(request, date):
    try:
        # Obținem data curentă și o ajustăm pentru ziua dorită
        current_date = datetime.now()
        event_date = current_date.replace(day=int(date), month=current_date.month, year=current_date.year)

        print(f"Data selectată: {event_date.date()}")
        # Căutăm toate programele care au data de start în acea zi
        events = Program.objects.filter(start_time__date=event_date.date())

        print(f"Evenimente găsite: {events}")

    except ValueError:
        events = []

    print(f"Evenimente găsite: {events}")
    
    # Returnăm template-ul cu informațiile despre eveniment
    return render(request, 'event_details.html', {'events': events})

