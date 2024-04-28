from django.urls import path
from . import views
from django.conf import settings #importa la configuración de Django (nuestra app central MedeBase)
from django.contrib.staticfiles.urls import static

# urlpatterns = [
#     path('',views.login, name='login'),
#     path("registro/", views.registro,name="registro"), 
#     path('perfil/', views.perfil_usuario, name='perfil_usuario'),
#     path('logout/', views.cerrar_sesion, name='logout'),
#     path('verificar-sesion/', views.verificar_sesion, name='verificar_sesion'),
# ] 