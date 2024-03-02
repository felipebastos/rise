from django.urls import path

from ghevent.views import add_inscrito_gh, event, home, remove_inscrito_gh, startnewgh

urlpatterns = [
    path("", home, name="gh"),
    path("start/", startnewgh, name="startnewgh"),
    path("<id>/add/", add_inscrito_gh, name="add_inscrito_gh"),
    path("<id>/remove/<eid>/", remove_inscrito_gh, name="remove_inscrito_gh"),
    path("<id>/", event, name="ghevent"),
]
