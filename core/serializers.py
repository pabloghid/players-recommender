from rest_framework import serializers
from .models import PlayersList
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class PlayerSerializer(serializers.Serializer):
    Id = serializers.IntegerField()
    Name = serializers.CharField()
    Team = serializers.CharField()    
    Age = serializers.IntegerField()
    Goals = serializers.FloatField()
    Assists = serializers.FloatField()
    Position = serializers.CharField()
    player_photo = serializers.CharField()
    player_team_logo = serializers.CharField()
    player_league_name = serializers.CharField()
    Duels_Total = serializers.IntegerField()
    Goals_Assist = serializers.IntegerField()
    Goals_Total = serializers.IntegerField()
    Games = serializers.IntegerField()
    Minutes = serializers.FloatField()
    Nationality = serializers.CharField()
    Accuracy_Passes = serializers.IntegerField()
    Key_Passes = serializers.IntegerField()
    Key_Passes_n = serializers.CharField()
    Total_Passes = serializers.IntegerField()
    Dribbles_Attempts = serializers.IntegerField()
    Dribbles_Success = serializers.IntegerField()
    Fouls_Drawn = serializers.IntegerField()
    Passes_Total_n = serializers.CharField()
    Dribbles_Success_Percentage = serializers.IntegerField()
    ## ataque
    Shots_On = serializers.IntegerField()
    Shots_Total = serializers.IntegerField()
    Shots = serializers.CharField()
    ShotsOnTarget = serializers.CharField()
    ShotsOnTarget_Percentage = serializers.IntegerField()
    Goals_Shot = serializers.CharField()
    Goals_ShotsOnTarget = serializers.CharField()
    ## defesa
    Fouls_Committed = serializers.IntegerField()
    Tackled_Block = serializers.IntegerField()
    Tackled_Intercept = serializers.IntegerField()
    Tackled_Total = serializers.IntegerField()
    Duels_Won = serializers.IntegerField()
    Duels_Total = serializers.IntegerField()
    Tackles = serializers.CharField()
    Blocks = serializers.CharField()
    Interceptations = serializers.CharField()
    Tackles_Interceptations = serializers.CharField()
    Duels_Won_Percentage = serializers.IntegerField()  
class PlayerNeighborSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    team = serializers.CharField()
    distance = serializers.FloatField()

class SimilarPlayersSerializer(serializers.Serializer):
    player = serializers.DictField(child=serializers.CharField())
    neighbors = PlayerNeighborSerializer(many=True)

class FavoritePlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayersList
        fields = '__all__'