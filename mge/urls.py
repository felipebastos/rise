from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("startnew/", views.startnew, name="startnew"),
    path("view/<id>/", views.mgeedit, name="mgeedit"),
    path("inscrever/<id>/", views.inscrever, name="inscrever"),
    path(
        "desinscrever/<id>/<player_id>/",
        views.desinscrever,
        name="desinscrever",
    ),
    path("addtorank/<id>/<player_id>/", views.addtorank, name="addtorank"),
    path(
        "removefromrank/<id>/<player_id>/",
        views.removefromrank,
        name="removefromrank",
    ),
    path("punir/<player_id>/", views.punir, name="punir"),
    path("despunir/<id>/<player_id>/", views.despunir, name="despunir"),
    path("punirPoder/<playerId>/", views.punirEventoDePoder, name="punirPoder"),
]
