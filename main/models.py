from django.db import models

# Create your models here.
class PlayerProfile(models.Model):
    steam_id = models.CharField(max_length=20, unique=True)
    guid = models.CharField(max_length=36, unique=True)
    name = models.CharField(max_length=100)
    tribe = models.ForeignKey('Tribe', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.name

class Tribe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    guid = models.CharField(max_length=36, unique=True)
    
    def __str__(self):
        return self.name
    
class Creature(models.Model):
    name = models.CharField(max_length=100)
    guid = models.CharField(max_length=36, unique=True)
    species = models.CharField(max_length=150)
    owner = models.ForeignKey(PlayerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='tamed_creatures')

    def __str__(self):
        return f"{self.name} ({self.species})"

class DodoBallMatch(models.Model):
    admin_creator = models.CharField(max_length=20)
    net_id_a = models.CharField(max_length=20)
    net_id_b = models.CharField(max_length=20)
    team_a_name = models.CharField(max_length=100)
    team_a_points = models.IntegerField()
    team_b_name = models.CharField(max_length=100)
    team_b_points = models.IntegerField()
    match_date = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Team A: {self.team_a_points} - Team B: {self.team_b_points} on {self.match_date}"