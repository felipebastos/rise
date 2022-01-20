"""rise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import logout
from django.urls import include, path

from rise import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.logar, name='logar'),
    path('logout/', views.sair, name='sair'),
    path('players/', include('players.urls')),
    path('admin/', admin.site.urls),
    path('bank/', include('bank.urls')),
    path('kvk/', include('kvk.urls')),
    path('mge/', include('mge.urls')),
    path('reports/', include('reports.urls')),
    path('captcha/',include("captcha.urls")),
]

admin.site.site_header  =  "K32 Admin"  
admin.site.site_title  =  "Administração do K32"
admin.site.index_title  =  "K32 Admin"
