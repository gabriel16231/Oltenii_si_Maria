
from django.shortcuts import render, get_object_or_404
from .models import Event
from .models import Program
from datetime import datetime
from django.contrib import messages

def calendar_view(request):
    days = range(1, 31)  # Zilele 1-31
    programs = Program.objects.all()  # Preia toate programele din baza de date
    events = []
    
    # Creează un obiect de eveniment pentru fiecare program
    for program in programs:
        event = {
            'date': program.start_time.date(),
            'title': program.task.description,  # Titlul din task (sau alt câmp relevant)
            'description': program.task.category,  # Descrierea din task (sau alt câmp relevant)
            'category': program.task.category  # Categoria din task
        }
        events.append(event)

    return render(request, 'calendar.html', {'days': days, 'events': events})


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

