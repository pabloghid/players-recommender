from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('get_player_recommendation/<int:player_id>/', get_player_recommendation, name='get_player_recommendation'),
    path('players', players, name='players'),
]