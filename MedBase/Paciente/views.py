from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistroForm
from  .models import Paciente  # Importa model Paciente
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')

def login(request):
    return render(request, 'paciente/login.html')

def registro(request):
    print("Ejecutando registro...")
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            print("CURP:", form.cleaned_data['curp'])
            print("Email:", form.cleaned_data['email'])
            print("Nombres:", form.cleaned_data['nombres'])
            print("Apellido Paterno:", form.cleaned_data['apellidoPaterno'])
            print("Apellido Materno:", form.cleaned_data['apellidoMaterno'])

            paciente = form.save(commit=False)
            paciente.set_password(form.cleaned_data['password'])
            print("si funcionoooo wtffffffff")
            paciente.save()
            print("Si se guardo aaaaaaaaaaaaa")
            
            return redirect('login') #lo cambie a que redirija al login
    else:
        form = RegistroForm()
    
    return render(request, 'paciente/registro.html', {'form': form})
