from django.shortcuts import redirect, render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Turno, User
from .serializers import TurnoSerializer, UserSerializer
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]


def registerPage(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario en la base de datos
            return redirect('/')  # Redirige a la página de login o donde prefieras
    else:
        form = UserForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
