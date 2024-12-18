from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm

# Agrega esta importación para obtener el nombre del backend de autenticación
from django.conf import settings

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el nuevo usuario en la base de datos.
            user.refresh_from_db()  # Recarga la instancia del usuario desde la base de datos.
            # Especifica explícitamente el backend de autenticación
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)  # Inicia sesión con el usuario recién creado.
            return redirect('core:home')  # Redirige al usuario a la página 'home'.
    else:
        form = SignupForm()
    return render(request, 'usuarios/signup.html', {'form': form})

# login page
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

# logout page
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


def ajustes_view(request):
    contexto = {'mensaje': "Hola, mundo. Este es mi contexto."}
    return render(request, 'usuarios/ajustes.html', contexto)