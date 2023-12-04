from django.urls import path

from .views import *

urlpatterns = [
    path('players/', PlayerListAPI.as_view(), name='player-list'),
    path('players/<int:player_id>/', PlayerDetailAPI.as_view(), name='player-detail'),
    path('players/similar/<int:player_id>/', SimilarPlayersAPI.as_view(), name='similar-players'),
    path('player-list/', FavoritePlayersListView.as_view(), name='favorite-players'),
    path('player-list/<int:pk>/', FavoritePlayersDetailView.as_view(), name='favorite-player-remove'),
    path('register/', RegisterAPIView.as_view(), name='register-view'),
    path('user/', UserInfoAPIView.as_view(), name='user-info'),
    path('is-player-in-favorites/<int:player_id>/', IsPlayerInFavoritesView.as_view(), name='is-player-in-favorites'),
]