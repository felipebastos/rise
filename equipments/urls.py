from django.urls import path

from equipments import views

urlpatterns = [
    path("", views.home, name="equip_home"),
    path("add/", views.add_equip, name="equip_add"),
    path("sets/", views.conjuntos, name="conjunto_add"),
]
