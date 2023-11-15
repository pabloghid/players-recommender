from django.shortcuts import render
from django.http import HttpResponse
from .services import PlayerRecommendation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .serializers import PlayerSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

player_rec = PlayerRecommendation()
player_rec.initialize()

class PlayerListAPI(APIView):
    def get(self, request):
        players = player_rec.get_all_players()  # Obtenha seus dados de jogadores (do DataFrame pandas)
        serialized_players = PlayerSerializer(players, many=True)
        return Response(serialized_players.data, status=status.HTTP_200_OK)
    
class PlayerDetailAPI(APIView):
    def get(self, request, player_id):
        player = player_rec.get_player_by_id(player_id) 
        if player is not None:
            serialized_player = PlayerSerializer(player)
            return Response(serialized_player.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SimilarPlayersAPI(APIView):
    def get(self, request, player_id):
        similar_players_data = player_rec.find_player_neighbors(player_id)
        return Response(similar_players_data, status=status.HTTP_200_OK)
    