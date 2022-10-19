from django.urls import path

from tasks import views

urlpatterns = [
    path("", views.home, name="tasks_home"),
    path("execute/<uuid>/", views.execute_task, name="execute_task"),
    path("remove/<uuid>/", views.remove_task, name="remove_task"),
]
