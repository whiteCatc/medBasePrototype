from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistroForm
from  .models import Paciente  # Importa model Paciente
from .forms import LoginForm
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse("Usuario Autenticado")
            else:
                return HttpResponse("La informacion no es correcta")
    #return render(request, 'paciente/login.html')

    else:
        form = LoginForm()
        return render(request, 'paciente/login.html', {'form':form})

def registro(request):
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.set_password(form.cleaned_data['password'])
            paciente.save()

            return redirect('login') #lo cambie a que redirija al login
    else:
        form = RegistroForm()
    
    return render(request, 'paciente/registro.html', {'form': form})