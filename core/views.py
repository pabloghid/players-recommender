from .services import PlayerRecommendation
from .models import PlayersList
from .serializers import PlayerSerializer, FavoritePlayersSerializer, UserSerializer
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

player_rec = PlayerRecommendation()
player_rec.initialize()

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Este nome de usuário já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def post(self, request):
        request.auth.delete()
        return Response({"detail": "Logout realizado com sucesso."})
    
class PlayerListAPI(APIView):
    def get(self, request):
        players = player_rec.get_all_players()
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
    
class FavoritePlayersListView(generics.ListCreateAPIView):
    queryset = PlayersList.objects.all()
    serializer_class = FavoritePlayersSerializer

    def list(self, request, *args, **kwargs):
        # Listar apenas os jogadores do usuário autenticado
        queryset = PlayersList.objects.filter(user=request.user)
        serializer = FavoritePlayersSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Adicionar jogador à lista do usuário autenticado
        request.data['user'] = request.user.id
        serializer = FavoritePlayersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoritePlayersDetailView(generics.RetrieveDestroyAPIView):
    queryset = PlayersList.objects.all()
    serializer_class = FavoritePlayersSerializer

    def get_object(self):
        # Obter jogador da lista do usuário autenticado por player_id
        player_id = self.kwargs['player_id']
        obj = PlayersList.objects.get(user=self.request.user, player_id=player_id)
        return obj