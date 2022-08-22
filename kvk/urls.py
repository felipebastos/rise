from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="kvk_index"),
    path("createkvk/", views.new_kvk, name="new_kvk"),
    path("edit/<kvkid>/", views.show_kvk, name="show_kvk"),
    path("close/<kvk_id>/", views.close_kvk, name="close_kvk"),
    path("zerado/<player_id>/", views.add_zerado, name="add_zerado"),
    path(
        "removezerado/<kvk>/<zerado_id>/",
        views.removezerado,
        name="removezerado",
    ),
    path(
        "analise/<kvkid>/<cat>/",
        views.analisedesempenho,
        name="analisedesempenho",
    ),
    path("adicionarfarm/", views.adicionarFarms, name="adicionarFarms"),
    path("etapa/<kvkid>/", views.registrarEtapa, name="registrarEtapa"),
    path("upload/<kvkid>/", views.etapas_por_planilha, name="registrarEtapasPorPlanilha"),
    path("clearetapa/<kvkid>/", views.clear_etapas, name="limparetapas"),
]
