from django.shortcuts import render, redirect
from django.http import HttpResponse
from  .models import Paciente  # Importa model Paciente
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')

def login(request):
    return render(request, 'paciente/login.html')

def registro(request):
    return render(request, 'paciente/registro.html')