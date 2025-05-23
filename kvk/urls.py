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
    path("removecargo/<cargoid>/", views.remove_cargo, name="remove_cargo"),
    path("config/<kvkid>/", views.config_kvk, name="config_kvk"),
    path("consolidar/<kvkid>/", views.consolidar_kvk, name="consolidar_kvk"),
    path("dkp/<kvkid>/", views.dkp_view, name="dkp_view"),
    path("dkp/<kvkid>/status/<player>/", views.status_dkp, name="status_dkp"),
    path("dkp/<kvkid>/upload/", views.upload_hoh_csv, name="upload_hoh"),
]
