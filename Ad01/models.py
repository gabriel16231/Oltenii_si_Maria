from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    type = models.CharField(max_length=32, default="Full Time")
    salary = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    
