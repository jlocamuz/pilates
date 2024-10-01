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

    def has_role(self, role):
        return self.role == role

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
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )

    HORA_CHOICES = [(f"{hour:02}:00", f"{hour:02}:00") for hour in range(7, 22)]  # De 07:00 a 21:00

    dia = models.CharField(max_length=9, choices=DIA_CHOICES, default='Lunes')
    hora = models.CharField(max_length=5, choices=HORA_CHOICES, default='17:00')
    max_alumnos = models.IntegerField(default=6)

    def __str__(self):
        return f"{self.dia} a las {self.hora}"

    def camillas_disponibles(self):
        return self.max_alumnos - self.alumnos.count()

    def liberar_plaza(self, alumno):
        if alumno in self.alumnos.all():
            self.alumnos.remove(alumno)
        else:
            raise ValueError(f"El alumno {alumno.username} no está registrado en este turno.")

    def reprogramar_turno(self):
        semana_actual = self.fecha.isocalendar()[1]
        return Turno.objects.filter(
            fecha__week=semana_actual,
            max_alumnos__gt=models.F('alumnos__count')
        ).exclude(id=self.id)

    @classmethod
    def turnos_en_mes(cls, year, month):
        turnos_del_mes = {}
        _, num_days = calendar.monthrange(year, month)

        for day in range(1, num_days + 1):
            current_date = timezone.datetime(year, month, day)
            day_name = current_date.strftime("%A")
            turnos = cls.objects.filter(dia=day_name)
            if turnos.exists():
                turnos_del_mes[current_date] = turnos
        return turnos_del_mes

    @classmethod
    def crear_turnos(cls):
        """Crea turnos automáticamente para cada día y cada horario."""
        dias = dict(cls.DIA_CHOICES)
        for dia in dias.keys():
            for hora in [h[0] for h in cls.HORA_CHOICES]:
                cls.objects.get_or_create(dia=dia, hora=hora, defaults={'max_alumnos': 6})
