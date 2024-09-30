from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Extend the default User model if necessary
    is_admin = models.BooleanField(default=False)

class Turno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos')
    dia = models.CharField(max_length=20)  # e.g., Lunes, Martes
    hora = models.TimeField()  # e.g., 16:00
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.dia} a las {self.hora} para {self.user.username}'
