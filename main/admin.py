from django.contrib import admin
from .models import PlayerProfile, Tribe, Creature, DodoBallMatch, AdminAnnouncement

# Register your models here.
admin.site.register(PlayerProfile)
admin.site.register(Tribe)
admin.site.register(Creature)
admin.site.register(DodoBallMatch)
admin.site.register(AdminAnnouncement)
