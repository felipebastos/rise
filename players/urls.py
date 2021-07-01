from django.urls import path

from . import views

urlpatterns = [
    path('<int:game_id>/', views.index, name='index'),
    path('populate', views.populate, name='populate'),
]
