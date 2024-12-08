from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.db import IntegrityError
from .models import User, Program, Task
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.
def live_tasks(request):
    u = request.user
    users_under_manager = User.objects.filter(manager=u.username)

    on_tasks = Program.objects.filter(user__in=users_under_manager, active=True)
    off_tasks = Program.objects.filter(user__in=users_under_manager, active=False)

    return render(request, "live_tasks.html", {
        "is_admin":True,
        "nume": u.last_name,
        "prenume": u.first_name,
        "on_tasks": on_tasks,
        "off_tasks": off_tasks,
    })

def view_angajati(request):
    u = request.user
    all_angajati = User.objects.filter(manager=u.username).exclude(username=u.username)

    return render(request, "view_angajati.html", {
        "is_admin":True,
        "nume": u.last_name,
        "prenume": u.first_name,
        "all_angajati": all_angajati,
        "detalii":None
    })

def detalii_angajati(request,u):
    user = request.user
    all_angajati = User.objects.filter(manager=user.username).exclude(username=user.username)
    detalii = User.objects.get(username=u)

    return render(request, "view_angajati.html",{
        "is_admin":True,
        "nume": user.last_name,
        "prenume": user.first_name,
        "all_angajati": all_angajati,
        "detalii": detalii
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            user = User.objects.get(username =  username);
            print(user.type == "admin")
            if user.type == "admin": return redirect('/liveTasks/')
            else: return render(request, "layout.html",{
            "is_admin":False,
            "nume": request.user.last_name,
            "prenume": request.user.first_name,
        })
           
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        nume = request.POST["nume"]
        prenume = request.POST["prenume"]
        id = request.POST["manager"]
        tip = request.POST["user_type"]
        
        if tip == "admin": salary = 5000
        elif tip == "full_time" : salary = 3800
        else: salary = 1500;

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, 
                password=password, 
                first_name=prenume, 
                last_name=nume,  
                email=email,
                type=tip, 
                salary= salary,
                manager = id
            )
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        
        if tip == "admin" : return redirect('/liveTasks/')
        else :return render(request, "layout.html",{
            "is_admin":False,
            "nume": request.user.last_name,
            "prenume": request.user.first_name,
        })
    else:
        return render(request, "register.html")