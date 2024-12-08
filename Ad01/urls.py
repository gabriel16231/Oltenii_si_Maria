from django.urls import path
from . import views3
from . import views2,views1

urlpatterns = [
    path("",views3.login_view,name="login"),
    path("register",views3.register,name="register"),
    path("logout",views3.logout_view,name="logout"),
    path("userpage",views2.user_page, name="user_page"),
    path("scheduled_tasks",views2.schedule,name="schedule"),
    path("show_c",views2.show_c,name="showc"),
    path('task-dropdown', views2.task_dropdown, name='task_dropdown'),
    path('add-task/', views2.add_task, name='add_task'),
    path('create-program', views2.create_program, name='create_program'),
    path("liveTasks/", views3.live_tasks, name="liveTasks"),
    path("Angajati/", views3.view_angajati, name="Angajati"),
    path("detalii/<str:u>",views3.detalii_angajati, name="detalii"),
    path('calendar', views1.calendar_view, name='calendar_view'),  # Ruta pentru pagina principală a calendarului
    path('calendar/<int:month>/<int:year>/', views1.calendar_view, name='calendar'),  # pagina pentru lună specifică
    path('events/<int:date>/', views1.event_details, name='event_details')
    #path("liveTasks", views3.liveTasks, name="liveTasks")
]