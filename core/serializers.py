from rest_framework import serializers

class PlayerSerializer(serializers.Serializer):
    Id = serializers.IntegerField()
    Name = serializers.CharField()
    Team = serializers.CharField()    
    Age = serializers.IntegerField()                                          

class PlayerNeighborSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    team = serializers.CharField()
    distance = serializers.FloatField()

class SimilarPlayersSerializer(serializers.Serializer):
    player = serializers.DictField(child=serializers.CharField())
    neighbors = PlayerNeighborSerializer(many=True)