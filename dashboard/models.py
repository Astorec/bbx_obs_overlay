from django.db import models

class Participants(models.Model):
    participant_id = models.IntegerField(primary_key=False)
    group_id = models.IntegerField(null=True)
    name = models.CharField(max_length=256)
    tournament_id = models.IntegerField()
    challonge_username = models.CharField(max_length=256, null=True)
    username = models.CharField(max_length=256, null = True)
    
class Tournaments(models.Model):
    tournament_id = models.IntegerField(primary_key=False)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=9999)
    created_at = models.DateField()
    state = models.CharField(max_length=256)
    swiss_rounds = models.IntegerField()
    started_at = models.DateField()
    start_at = models.DateField(null=True)
    participants_locked = models.BooleanField()
    participants_swappable = models.BooleanField()
    
class Matches(models.Model):
    match_id = models.IntegerField(primary_key=False)
    identifier = models.CharField(max_length=1)
    player1_id = models.IntegerField()
    player2_id = models.IntegerField()
    state = models.CharField(max_length=256)
    round = models.IntegerField()
    loser_id = models.IntegerField(null=True)
    group_id = models.IntegerField(null=True)
    tournament_id = models.IntegerField()
    
class Settings(models.Model):
    api_key = models.CharField(max_length=256)
    username = models.CharField(max_length=256)