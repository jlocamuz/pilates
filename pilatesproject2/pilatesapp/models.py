from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import calendar

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('profesor', 'Profesor'),
        ('alumno', 'Alumno'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Turno(models.Model):
    profesor = models.ForeignKey(
        User, 
        limit_choices_to={'role': 'profesor'}, 
        on_delete=models.CASCADE, 
        related_name='turnos_como_profesor'
    )
    alumnos = models.ManyToManyField(
        User, 
        limit_choices_to={'role': 'alumno'}, 
        blank=True, 
        related_name='turnos_como_alumno'
    )

    DIA_CHOICES = (
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),

    )

    HORA_CHOICES = [(f"{hour:02}:00", f"{hour:02}:00") for hour in range(7, 22)]  # De 07:00 a 21:00

    dia = models.CharField(max_length=9, choices=DIA_CHOICES, default='Lunes')
    hora = models.CharField(max_length=5, choices=HORA_CHOICES, default='17:00')
    max_alumnos = models.IntegerField(default=6)

    def __str__(self):
        return f"{self.dia} a las {self.hora}"

    