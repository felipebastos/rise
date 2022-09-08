from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="bank_index"),
    path("createweek/<tag>/<resource>/", views.create_week, name="create_week"),
    path("week/<weekid>/", views.week, name="week"),
    path("donated/<donationid>/", views.donated, name="donated"),
    path("report/", views.donations_report, name="report"),
    path(
        "register/donations/<weekid>/",
        views.register_week,
        name="registrar_doacao",
    ),
    path("creditos/", views.add_credits, name="creditos"),
]
