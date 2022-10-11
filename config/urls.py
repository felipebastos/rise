from django.urls import path

from config import views

urlpatterns = [
    path("", views.home, name="config"),
]
