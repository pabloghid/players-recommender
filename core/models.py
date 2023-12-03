from django.db import models
from django.contrib.auth.models import User

class PlayersList(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id =  models.IntegerField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)