from django.db import models

# Create your models here.
class PlayerProfile(models.Model):
    steam_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    tribe = models.ForeignKey('Tribe', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.name

class Tribe(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Creature(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=150)
    owner = models.ForeignKey(PlayerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='tamed_creatures')

    def __str__(self):
        return f"{self.name} ({self.species})"