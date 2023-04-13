from django.urls import path

from osiris import views

urlpatterns = [
    path("", views.home, name="arca_home"),
    path("time/remove/<funcaoid>/", views.remove_funcao, name="remove_do_time"),
    path("time/<timeid>/", views.editar_time, name="editar_time"),
    path(
        "marchas/<funcaoid>/",
        views.configurar_marchas,
        name="configurar_marchas",
    ),
    path("marcha/remove/<marchaid>/", views.remove_marcha, name="marcha_remove"),
]
