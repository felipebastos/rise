from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="mge_index"),
    path("startnew/", views.startnew, name="startnew"),
    path("view/<mge_id>/", views.mgeedit, name="mgeedit"),
    path("inscrever/<mge_id>/", views.inscrever, name="inscrever"),
    path(
        "desinscrever/<mge_id>/<player_id>/",
        views.desinscrever,
        name="desinscrever",
    ),
    path("addtorank/<mge_id>/<player_id>/", views.addtorank, name="addtorank"),
    path(
        "removefromrank/<mge_id>/<player_id>/",
        views.removefromrank,
        name="removefromrank",
    ),
    path("punir/<player_id>/", views.punir, name="punir"),
    path("despunir/<mge_id>/<player_id>/", views.despunir, name="despunir"),
    path(
        "punirPoder/<player_id>/",
        views.punir_evento_de_poder,
        name="punirPoder",
    ),
]
