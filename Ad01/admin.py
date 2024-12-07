from django.contrib import admin
from .models import User,Program,Task

# Register your models here.
admin.site.register(User)
admin.site.register(Program)
admin.site.register(Task)