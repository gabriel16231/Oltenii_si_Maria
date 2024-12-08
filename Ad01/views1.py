
from django.shortcuts import render, get_object_or_404
from .models import Program
from datetime import datetime
from django.contrib import messages
from collections import defaultdict

def calendar_view(request, month=None, year=None):
    u=request.user;
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

    return render(request, 'scheduled_tasks.html', {
        
        'month_name': month_name,
        'events': events,
        'days': valid_days,
        'current_month': month,
        'current_year': year,
        "is_admin":True,
        "nume": u.last_name,
        "prenume": u.first_name,# Pass all programs to the template
        "hide_add":True,
        "hide_dd":True
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

def task_approval(request):
    # Verificăm dacă există cheia 'date' în POST
    u = request.user
    if 'date' not in request.POST:
        return render(request, 'task_approval.html', {'error': 'Data nu a fost furnizată.'})

    # Obținem data din POST
    date = request.POST["date"]

    hour = None  # Valoare implicită pentru ora
    if u.type == "full_time" and 'time' in request.POST:  # Verificăm dacă 'time' există în POST
        hour = request.POST["time"]
        print("H: ", hour)

    start_time = None  # De exemplu, start_time poate fi None pentru întreaga zi
    duration_minutes = None  # Pentru întreaga zi (24 de ore)

    # Apelăm funcția get_programs_in_time_range pentru a obține programele
    task_list = get_programs_in_time_range(date, hour, duration_minutes).filter(user__isnull=True).order_by('start_time')

    # Creăm un defaultdict pentru a grupa taskurile pe ore
    tasks_by_hour = defaultdict(list)
    for task in task_list:
        hour = task.start_time.hour  # Extragem ora de start a fiecărui task
        tasks_by_hour[hour].append(task)

    print("Tasks by hour: ", tasks_by_hour)

    checked_list = []

    if request.method == "POST":
        checked_list = request.POST.getlist('programs')
        # Aici adăugați logica pentru procesarea datelor postate

        # Setăm userul pentru fiecare program selectat
       
        for task_id in checked_list:
            task = Program.objects.filter(id=task_id).first()  # Găsim programul după ID
            if task:  # Verificăm dacă task-ul există
                task.user = u  # Setăm userul
                task.save()  # Salvăm modificările

        ft = False
        if u.type == "full_time":
            ft = True

    # Transmiterea task_list și tasks_by_hour către template
    return render(request, 'task_approval.html', {
        'tasks_by_hour': dict(tasks_by_hour),
        'checked_list': checked_list if 'checked_list' in locals() else [],
        'ft': ft
    })

from datetime import datetime, timedelta, time

def get_programs_in_time_range(date_str, start_time=None, duration_minutes=None):
    print(f"Start time received: {start_time}")  # Verifică ce valoare are start_time
    try:
        # Converim data din string în obiect de tip date
        filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Data nu este într-un format valid.")
    
    # Setăm valori implicite dacă nu sunt furnizate
    if start_time is None:
        start_time = time(0, 0)  # Ora 00:00 (obiect time)
    elif isinstance(start_time, str):  # Dacă start_time este un string, îl convertim într-un obiect time
        start_time = datetime.strptime(start_time, "%H:%M").time()
    
    if duration_minutes is None:
        duration_minutes = 1440  # 24 ore, întreaga zi
    
    # Calculăm intervalul de timp
    start_datetime = datetime.combine(filter_date, start_time)  # Combinăm data și ora de start
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)

    # Filtrăm programele care se încadrează în intervalul dat
    programs_in_range = Program.objects.filter(
        start_time__gte=start_datetime,
        start_time__lt=end_datetime
    )
    
    return programs_in_range


