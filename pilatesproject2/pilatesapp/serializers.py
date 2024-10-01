from rest_framework import serializers
from .models import User, Turno

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'username')  # Agrega los campos que necesites



class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
            model = Turno
            fields = ['id', 'profesor', 'alumnos', 'dia', 'hora']