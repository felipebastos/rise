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
    path("adicionarfarm/", views.adicionar_farms, name="adicionarFarms"),
    path("adicionarmge/", views.adicionar_mge_controlado, name="adicionarMGE"),
    path("etapa/<kvkid>/", views.registrar_etapa, name="registrarEtapa"),
    path(
        "upload/<kvkid>/",
        views.etapas_por_planilha,
        name="registrarEtapasPorPlanilha",
    ),
    path("clearetapa/<kvkid>/", views.clear_etapas, name="limparetapas"),
    path("cargos/<kvkid>/", views.cargos_view, name="cargos_view"),
]
