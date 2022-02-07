from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createkvk/", views.new_kvk, name="new_kvk"),
    path("edit/<kvkid>/", views.show_kvk, name="show_kvk"),
    path("close/<kvk_id>/", views.close_kvk, name="close_kvk"),
    path("zerado/<player_id>/", views.add_zerado, name="add_zerado"),
    path(
        "removezerado/<kvk>/<zerado_id>/",
        views.removezerado,
        name="removezerado",
    ),
    path("analise/<kvkid>/", views.analisedesempenho, name="analisedesempenho"),
]
