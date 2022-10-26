from django.urls import path

from equipments import views

urlpatterns = [
    path("", views.home, name="equip_home"),
]
