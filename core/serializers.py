from rest_framework import serializers
from .models import PlayersList
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
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

    ## Goleiro
    Save_Percentage = serializers.IntegerField()  ## 
    Goals_Conceded = serializers.IntegerField()  
    Goals_Saves = serializers.IntegerField()  
    Goals_Conceded_n = serializers.CharField()    ##

    ## outros
    Ninety_S = serializers.IntegerField(source='90s')
    Rating = serializers.FloatField()
    Yellow_Cards = serializers.CharField()
    Red_Cards = serializers.CharField()
    Yellow_Red_Cards = serializers.CharField()
    Weight_kg = serializers.IntegerField()
    Height_cm = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if 'Rating' in data and data['Rating'] is not None:
            data['Rating'] = round(data['Rating'], 2)
        if 'Height_cm' in data and data['Height_cm'] is not None:
            data['Height_cm'] = data['Height_cm']/100
            data['Height_cm'] = round(data['Height_cm'], 2)


        return data
class PlayerNeighborSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    team = serializers.CharField()
    distance = serializers.FloatField()

class SimilarPlayersSerializer(serializers.Serializer):
    player = serializers.DictField(child=serializers.CharField())
    neighbors = PlayerNeighborSerializer(many=True)

class FavoritePlayersSerializer(serializers.ModelSerializer):
    player_name = serializers.SerializerMethodField()

    class Meta:
        model = PlayersList
        fields = ['id', 'player_id', 'user', 'created_at', 'updated_at', 'player_name']

    def __init__(self, *args, **kwargs):
        player_rec = kwargs.pop('player_rec', None)
        super().__init__(*args, **kwargs)
        self.player_rec = player_rec

    def get_player_name(self, obj):
        if self.player_rec and callable(getattr(self.player_rec, 'get_player_by_id', None)):
            player = self.player_rec.get_player_by_id(obj.player_id)
            if player:
                return player
        return None
    