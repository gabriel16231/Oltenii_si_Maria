from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    
    # Tipul utilizatorului (admin sau user)
    type = models.CharField(max_length=10)



    salary = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    manager= models.CharField(max_length=30)

class Task(models.Model):
    category = models.CharField(max_length=64)  # Categoria task-ului (ex: "Work", "Personal")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True)  # Ponderea task-ului, ex: 0.25 (25%)
    description = models.TextField(blank=True)


class Program(models.Model):
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # Duration in minutes
    required_people = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    manager= models.CharField(max_length=30)
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default='Medium')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True)

    def __str__(self):
        return f"Program pentru {self.task.category} - {self.task.description[:50]}"

    def get_end_time(self):
        """Calculăm ora de finalizare bazată pe ora de începere și durata."""
        if self.start_time and self.duration:
            return self.start_time + timedelta(minutes=self.duration)
        return None

    def save(self, *args, **kwargs):
        # Check if the start_time is today and match the time with current datetime
        if self.start_time:
            now = timezone.now()  # This will be an aware datetime
            # Calculate the end_time by adding the duration (in minutes) to the start_time
            end_time = self.get_end_time()
            
            if self.start_time.date() == now.date() and self.start_time.hour == now.hour and self.start_time.minute == now.minute:
                self.active = True
            elif end_time and now > end_time:
                # If the current time is after the end_time, set active to False
                self.active = False
            else:
                # If it's not the right time yet, set active to True
                self.active = False

        super(Program, self).save(*args, **kwargs)