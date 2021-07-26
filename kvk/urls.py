from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createkvk/', views.new_kvk, name='new_kvk'),
    path('edit/<kvk_id>/', views.show_kvk, name='show_kvk'),
    path('update/<kvk_id>/<player_id>/<honra>/<zerado>/', views.milestone_kvk, name='milestone_kvk'),
    path('close/<kvk_id>/', views.close_kvk, name='close_kvk'),
]