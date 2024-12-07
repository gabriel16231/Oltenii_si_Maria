from django.urls import path
from . import views3
from . import views2
from . import views1

urlpatterns = [
    path("",views3.login_view,name="login"),
    path("register",views3.register,name="register"),
    path("logout",views3.logout_view,name="logout"),
    path("userpage",views2.user_page, name="user_page"),
    #path("liveTasks", views3.liveTasks, name="liveTasks"),
    
    path('cal', views1.calendar_view, name='calendar_view'),  # Ruta pentru pagina principală a calendarului
    path('events/<int:date>/', views1.event_details, name='event_details')  # Ruta pentru detaliile evenimentelor
]
