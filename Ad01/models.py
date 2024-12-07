from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


class User(AbstractUser):
    pass

    TYPE_CHOICES = [
        ('admin', 'Manager'),
        ('user', 'Employee Full Time'),
        ('user', 'Employee Part Time')
    ]
    
    # Tipul utilizatorului (admin sau user)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)

    # Managerul unui utilizator (ForeignKey la User, null pentru admini)
    manager = models.ForeignKey(
        'self',  # 'self' se referă la User, pentru că managerul va fi tot un User
        on_delete=models.SET_NULL,  # Dacă managerul este șters, câmpul manager va fi setat pe null
        null=True,  # Permite ca managerul să fie null pentru admini
        blank=True,  # Permite să fie gol pentru admini
        related_name='employees'  # Permite să accesăm angajații unui manager (opțional)
    )

    salary = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)

class Task(models.Model):
    category = models.CharField(max_length=64)  # Categoria task-ului (ex: "Work", "Personal")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True)  # Ponderea task-ului, ex: 0.25 (25%)
    description = models.TextField(blank=True)

class Program(models.Model):
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)  # Legătură cu Task

    start_time = models.DateTimeField(null=True, blank=True)  # Opțional, poate fi lăsat necompletat
    duration = models.IntegerField(null=True, blank=True)  # Durata în minute (poți adăuga validări ulterioare dacă dorești)
    required_people = models.IntegerField(null=True, blank=True)   

    # Prioritatea taskului
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default='Medium')

    # Progresul taskului (în procent)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True)  # Valori de la 0.00 la 100.00

    def __str__(self):
        return f"Program pentru {self.task.category} - {self.task.description[:50]}"

    def get_end_time(self):
        """Calculăm ora de finalizare bazată pe ora de începere și durata."""
        if self.start_time and self.duration:
            return self.start_time + timedelta(minutes=self.duration)
        return None 