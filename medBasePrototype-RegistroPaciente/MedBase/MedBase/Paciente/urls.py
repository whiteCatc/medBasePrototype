from django.urls import path
from . import views
from django.conf import settings #importa la configuración de Django (nuestra app central MedeBase)
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('',views.inicio, name='inicio'),
    path('paciente/login',views.login_view, name='login'),
    path('paciente/registro',views.registro, name='registro'),
    #path('nosotros',views.nosotros, name='nosotros'),
] 