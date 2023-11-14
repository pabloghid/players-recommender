from django.db import models
from django.contrib.auth.models import User

class PlayersList(models.Model):
    player_id = models.IntegerField
    user_id = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)