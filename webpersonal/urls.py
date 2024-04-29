"""
URL configuration for webpersonal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as core_views
from portfolio import views as portfolio_views
from homePage import views as homePage_views
from account import views as account_views
from sesion import views as sesion_views

from django.conf import settings 

urlpatterns = [
    path('', homePage_views.index, name="home"),
    path('about/', core_views.about, name="about"),
    path('portfolio/', portfolio_views.portfolio, name="portfolio"),
    path('contact/', core_views.contact, name="contact"),
    path('admin/', admin.site.urls),
    path('index/', homePage_views.index, name="index"),
    path('account/', account_views.account, name="account"),
    path('information/', account_views.information, name="information"),
    path('plans/', account_views.plans, name="plans"),
    #sesion
    path('login/',sesion_views.login, name='login'),
    path("registro/", sesion_views.registro,name="registro"), 
    path('perfil/', sesion_views.perfil_usuario, name='perfil_usuario'),
    path('logout/', sesion_views.cerrar_sesion, name='logout'),
    path('verificar-sesion/', sesion_views.verificar_sesion, name='verificar_sesion'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
