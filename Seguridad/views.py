from django.urls import path
from django.shortcuts import render, redirect


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myadmin.models import Usuario

# Create your views here.

def index(request):
    


    if request.method == 'POST':
        usuario = request.POST['usuario']
        contraseña = request.POST['password']
        usuarioAutenticado = authenticate(request, username=usuario, password=contraseña)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.is_active:
                login(request, usuarioAutenticado)
                if request.user.is_authenticated:
                    user = request.user
                    grupos = user.groups.all()
                    if any(grupo.name == 'Administrador' for grupo in grupos):
                        # Usuario pertenece al grupo 'Grupo1'
                        return redirect('main/')
                    elif any(grupo.name == 'empleado' for grupo in grupos):
                        # Usuario pertenece al grupo 'Grupo2'
                        return redirect('user/')
            else:
                messages.error(request, 'Lamentablemente, tu cuenta ya no tiene acceso al sistema.')
        else:
            try:
                user = Usuario.objects.get(username=usuario)
                if not user.is_active:
                    # Usuario inactivo, mostrar mensaje de error
                    messages.error(request, 'Tu cuenta está bloqueada. Contacta al administrador.')
                else:
                    messages.error(request, 'El usuario o la contraseña son incorrectos. Intenta nuevamente')
            except Usuario.DoesNotExist:
                messages.error(request, 'El usuario o la contraseña son incorrectos. Intenta nuevamente')

    return render(request, 'login.html')

@login_required(login_url='login')
def cerrarSesion(request):
    logout(request)
    return redirect('login')