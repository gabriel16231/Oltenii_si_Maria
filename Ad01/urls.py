from django.urls import path
from . import views3

urlpatterns = [
    path("",views3.login_view,name="login"),
    path("register",views3.register,name="register"),
    path("logout",views3.logout_view,name="logout")
]