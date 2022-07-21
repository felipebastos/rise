from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("300/", views.top300, name="top300"),
    path("rev/", views.top300rev, name="top300rev"),
    path(
        "analise/<cat>/",
        views.analisedesempenho,
        name="analisedesempenho300",
    ),
]
