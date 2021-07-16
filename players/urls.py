from django.urls import path

from . import views

urlpatterns = [
    path('<int:game_id>/', views.index, name='index'),
    path('populate/', views.populate, name='populate'),
    path('alliance/<str:ally_tag>/', views.alliance, name='alliance'),
    path('edit/<game_id>/', views.edit_player, name='edit_player'),
    path('addstatus/<game_id>/', views.add_status, name='add_status'),
]
