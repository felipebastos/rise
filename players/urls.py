from django.urls import path

from . import views

urlpatterns = [
    path('<int:game_id>/', views.index, name='index'),
    path('populate/', views.populate, name='populate'),
    path('alliance/<str:ally_tag>/', views.alliance, name='alliance'),
    path('edit/<game_id>/', views.edit_player, name='edit_player'),
    path('addstatus/<game_id>/', views.add_status, name='add_status'),
    path('find/', views.findplayer, name='findplayer'),
    path('listspec/<spec>/', views.listspecs, name='listspec'),
    path('review/<ally_tag>/', views.review_players, name='reviewplayers'),
    path('top300/', views.top300, name='top300'),
    path('nostatus/<ally_tag>/', views.falta_status, name='falta_status'),
    path('old/<ally_tag>/', views.antigos, name='antigos'),
    path('statusedit/<status_id>/', views.editaStatus, name='edit_status'),
    path('statusdelete/<status_id>/', views.delete_status, name='delete_status'),
]
