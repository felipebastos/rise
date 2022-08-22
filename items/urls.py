from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="itemshome"),
    path("aprovar/<pedido_id>/", views.aprovar, name="aprovarpedido"),
    path("reprovar/<pedido_id>/", views.reprovar, name="reprovarpedido"),
    path(
        "cancelar/<pedido_id>/",
        views.cancelar_avaliacao,
        name="cancelaravaliacao",
    ),
]
