from django.urls import path

from equipments import views

urlpatterns = [
    path("", views.home, name="equip_home"),
    path("add/", views.add_equip, name="equip_add"),
]
