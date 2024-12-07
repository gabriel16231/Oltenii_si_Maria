from django.urls import path
from . import views3
from . import views2

urlpatterns = [
    path("",views3.login_view,name="login"),
    path("register",views3.register,name="register"),
    path("logout",views3.logout_view,name="logout"),
    path("userpage",views2.user_page, name="user_page"),
    path("liveTasks", views3.liveTasks, name="liveTasks")
]