from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect,render
from .models import Task,Program
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.conf import settings


def user_page(request):
    template = loader.get_template('layout.html')
    return HttpResponse(template.render())

def show_c(request):
    u=request.user;
    return redirect('calendar', month=12, year=2024)
    return render(request, "scheduled_tasks.html", {
        "is_admin":True,
        "nume": u.last_name,
        "prenume": u.first_name,
        "show_calendar":True,
        "hide_add":True,
        "hide_dd":True
        
    })
def schedule(request):
    u=request.user;
    return redirect('add_task')
    return render(request, "scheduled_tasks.html", {
        "is_admin":True,
        "nume": u.last_name,
        "prenume": u.first_name,
        "show_calendar":False,
        "hide_add":False,
        "hide_dd":True
    })


def task_dropdown(request):
     
    u=request.user;
    # Retrieve distinct categories from the Task model
    categories = Task.objects.values_list('category', flat=True).distinct()

    selected_category = request.GET.get('category')  # Get the selected category from the query params
    
    if selected_category:
        tasks = Task.objects.filter(category=selected_category)  # Get tasks filtered by the selected category
    else:
        tasks = Task.objects.all()  # If no category is selected, show all tasks
    
    return render(request, 'scheduled_tasks.html', {'categories': categories, 'tasks': tasks, "is_admin":True,
    "nume": u.last_name,
    "prenume": u.first_name,
    "show_calendar":False,
    "hide_add":True,
    "hide_dd":False})

def add_task(request):
    
    u=request.user;
    if request.method == 'POST':
        category = request.POST.get('category')
        weight = request.POST.get('weight')
        description = request.POST.get('description')

        # Create a new Task entry
        Task.objects.create(
            category=category,
            weight=weight,
            description=description
        )

        # Redirect to the task dropdown page or another page after saving
        return redirect('task_dropdown')  # Redirect to the same page or a list of tasks

    return render(request, 'scheduled_tasks.html',{"is_admin":True,
    "nume": u.last_name,
    "prenume": u.first_name,
    "show_calendar":False,
    "hide_add":False,
    "hide_dd":True})  # You can render the same page or a different one
    

def create_program(request):
    u=request.user;
    # Fetch all tasks to populate the dropdown
    tasks = Task.objects.all()

    # Check if it is a POST request to create a program
    if request.method == 'POST':
        task_id = request.POST.get('task')
        start_time = request.POST.get('start_time')
        duration = request.POST.get('duration')
        required_people = request.POST.get('required_people')

        # Validate inputs
        if not task_id:
            return HttpResponse("Please select a valid task.", status=400)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponse("Task not found.", status=400)

        try:
            # Convert start_time from string to naive datetime
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

            # Make the datetime timezone-aware
            if settings.USE_TZ:
                start_time = make_aware(start_time)

        except ValueError:
            return HttpResponse("Invalid start time format.", status=400)

        try:
            duration = int(duration)
        except (ValueError, TypeError):
            return HttpResponse("Invalid duration provided.", status=400)

    

        # Create a new Program entry
        try:
            program = Program.objects.create(
                task=task,
                start_time=start_time,
                duration=duration,
                manager = u.username,
            )
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

        # After creating the program, retrieve all programs to display
        programs = Program.objects.all()

        # Redirect to the same page with all programs
        return render(request, 'scheduled_tasks.html', {
            'tasks': tasks,
            'programs': programs,
            "is_admin":True,
            "nume": u.last_name,
            "prenume": u.first_name,# Pass all programs to the template
        })

    # For GET requests, retrieve all programs to display them as well
    programs = Program.objects.all()
    
    return render(request, 'scheduled_tasks.html', {
        'tasks': tasks,
        'programs': programs,"is_admin":True,
        "nume": u.last_name,
        "prenume": u.first_name,  # Pass all programs to the template
        
    })