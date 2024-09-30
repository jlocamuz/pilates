from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import User, Turno
from .serializers import UserSerializer, TurnoSerializer

# def email(request):    
#     subject = 'Thank you for registering to our site'
#     message = ' it  means a world to us '
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ['j.locamuz@alumno.um.edu.ar',]   
#     #send_mail( subject, message, email_from, recipient_list, fail_silently=False)  
#     return HttpResponse('email enviado desde jlocamuz@gmail.com')


# ViewSet para gestionar usuarios (solo admins pueden crear/editar usuarios)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# ViewSet para gestionar turnos
# ViewSet para gestionar turnos
class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer

    def get_queryset(self):
        # Los administradores ven todos los turnos, los usuarios solo los suyos
        if self.request.user.is_admin:
            return Turno.objects.all()
        return Turno.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Solo administradores pueden asignar turnos
        if self.request.user.is_admin:
            serializer.save()
        else:
            raise PermissionError("No tienes permisos para crear turnos.")

    def update(self, request, *args, **kwargs):
        # Obtener el objeto del turno que se quiere actualizar
        turno = self.get_object()

        # Verificar si el usuario tiene permisos para actualizar este turno
        if request.user.is_admin or turno.user == request.user:
            # Permitir que el administrador o el dueño del turno actualice los datos
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(turno, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            # Si el usuario no tiene permisos, devolver un error de permiso
            return Response({"detail": "No tienes permisos para actualizar este turno."}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        # Guardar los cambios del turno
        serializer.save()
