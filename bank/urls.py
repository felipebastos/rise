from django.urls import path

from . import views

urlpatterns = [
    path('createweek/<tag>/', views.create_week, name='create_week'),
]