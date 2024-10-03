from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * # Asegúrate de importar tu nuevo UserViewSet

router = DefaultRouter()
router.register(r'turnos', TurnoViewSet)
router.register(r'users', UserViewSet)  # Registra el UserViewSet

urlpatterns = [
    path('', include(router.urls)),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login' ),
    path('logout/', logoutUser , name='logout' ),

    path('home/', HomePage, name='home' )

]