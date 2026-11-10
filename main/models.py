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

class AdminAnnouncement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin Announcement at {self.created_at}"

from django.db import models

class ServerConfigRequest(models.Model):
    GAME_CHOICES = [
        ('ASA', 'ARK: Survival Ascended'),
        ('ASE', 'ARK: Survival Evolved'),
    ]
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private (Password Protected)'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Beacon Build'),
        ('in_progress', 'Building in Beacon'),
        ('deployed', 'Deployed to Host'),
        ('archived', 'Archived'),
    ]

    # Core Searchable Metadata
    requester_name = models.CharField(max_length=120, help_text="Discord handle or name")
    server_name = models.CharField(max_length=150)
    game_version = models.CharField(max_length=3, choices=GAME_CHOICES, default='ASA')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    server_password = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Array / Text Fields
    maps = models.JSONField(default=list, help_text="List of selected maps")
    mods_requested = models.TextField(blank=True, help_text="Requested Mod IDs or names")
    blacklisted_items = models.TextField(blank=True, help_text="Engrams/items to hide or disable")
    custom_notes = models.TextField(blank=True, help_text="Supply drops, dino spawns, or extra rules")

    # Full Structured Payload (Rates, Breeding, Stat Multipliers, QoL Toggles)
    config_payload = models.JSONField(
        default=dict,
        help_text="Complete JSON object containing rates, breeding, and stat arrays"
    )

    # Pre-compiled INI Strings for quick copy/export
    game_user_settings_ini = models.TextField(blank=True)
    game_ini = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "ARK Server Config Request"
        verbose_name_plural = "ARK Server Config Requests"

    def __str__(self):
        return f"[{self.game_version}] {self.server_name} ({self.requester_name}) - {self.get_status_display()}"