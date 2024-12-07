from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from .models import User
from django.http import HttpResponseRedirect

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render (request,"index.html")
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        nume = request.POST["nume"]
        prenume = request.POST["prenume"]
        id = request.POST["manager"]
        tip = request.POST["user_type"]
        
        if tip == "admin": salary = 5000
        elif tip == "fulltime" : salary = 3800
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
        return render(request, "index.html")
    else:
        return render(request, "register.html")