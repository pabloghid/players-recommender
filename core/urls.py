from django.urls import path

from .views import *

urlpatterns = [
    path('api/players/', PlayerListAPI.as_view(), name='player-list'),
    path('api/players/<int:player_id>/', PlayerDetailAPI.as_view(), name='player-detail'),
    path('api/players/similar/<int:player_id>/', SimilarPlayersAPI.as_view(), name='similar-players'),
]