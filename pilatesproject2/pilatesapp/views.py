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
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]


from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

def registerPage(request):
    if request.user.is_authenticated: 
        redirect('home')
    else: 
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)  # No guardamos aún en la BD
                # Asignar contraseña por defecto según el rol
                if user.role == 'alumno':
                    user.set_password('contraseña_para_alumnos')  # Cambia por la contraseña deseada
                elif user.role == 'profesor':
                    user.set_password('contraseña_para_profesores')  # Cambia por la contraseña deseada
                else:
                    user.set_password('contraseña_por_defecto')  # Contraseña general si es necesario
                
                user.save()  # Guardar el usuario en la base de datos con la contraseña asignada
                username_created = form.cleaned_data.get('username')

                # solo para ese request. cuales son los mensajes de ese request
                messages.success(request, 'Account was created for ' + username_created) 
                return redirect('login')  # Redirigir a la página de login o la que prefieras
        else:
            form = UserForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'YOU ARE HOME!') 
            return redirect('home')
        
        else: 
            messages.info(request, 'Username OR password is incorrect')
        

    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def HomePage(request): 
    context = {
        'username': request.user.username,  # Pass the username to the template
    }
    return render(request, 'accounts/home.html', context)


def logoutUser(request): 
    logout(request)
    return redirect('login')