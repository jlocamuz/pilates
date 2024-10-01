from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Turno, User
from .serializers import TurnoSerializer, UserSerializer
from django.utils import timezone
from django.db.models import F

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return Turno.objects.all()
        elif user.has_role('profesor'):
            return Turno.objects.filter(profesor=user)
        elif user.has_role('alumno'):
            return Turno.objects.filter(alumnos=user)
        return Turno.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def disponibles(self, request):
        turnos = Turno.objects.filter(max_alumnos__gt=F('alumnos__count'))
        serializer = self.get_serializer(turnos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancelar_turno(self, request, pk=None):
        turno = self.get_object()
        alumno = request.user
        if alumno in turno.alumnos.all():
            turno.alumnos.remove(alumno)
            return Response({'message': 'Te has dado de baja del turno y tu lugar ha sido liberado'}, status=200)
        return Response({'error': 'No estás registrado en este turno'}, status=400)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def reprogramar(self, request):
        alumno = request.user
        hoy = timezone.now().date()
        turnos_disponibles = Turno.objects.filter(
            dia=hoy.strftime("%A"),
            max_alumnos__gt=F('alumnos__count')
        ).exclude(alumnos=alumno)
        serializer = self.get_serializer(turnos_disponibles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def turnos_del_mes(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({"error": "Año y mes son requeridos"}, status=400)

        turnos = Turno.turnos_en_mes(int(year), int(month))
        return Response(turnos)
