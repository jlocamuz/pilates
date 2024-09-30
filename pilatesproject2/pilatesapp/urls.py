#from .views import email
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TurnoViewSet


# Crea una instancia del DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)  # Ruta para el ViewSet de usuarios
router.register(r'turnos', TurnoViewSet)  # Ruta para el ViewSet de turnos

urlpatterns = [
    path('', include(router.urls))
]
    #path("mail/",  email),

