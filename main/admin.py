from django.contrib import admin
from .models import PlayerProfile, Tribe, Creature, DodoBallMatch, AdminAnnouncement

# Register your models here.
admin.site.site_header = "Brontobyte Admin"
admin.site.site_title = "Brontobyte Admin"
admin.site.index_title = "Manage Brontobyte"


class FriendlyModelAdmin(admin.ModelAdmin):
	list_display = ("__str__",)
	list_per_page = 25

	def get_search_fields(self, request):
		return tuple(
			field.name
			for field in self.model._meta.get_fields()
			if getattr(field, "get_internal_type", lambda: "")() in ("CharField", "TextField")
		)

	def get_list_filter(self, request):
		filterable_types = ("BooleanField", "DateField", "DateTimeField", "ForeignKey", " choices")
		return tuple(
			field.name
			for field in self.model._meta.get_fields()
			if getattr(field, "get_internal_type", lambda: "")() in filterable_types
		)


for model in (PlayerProfile, Tribe, Creature, DodoBallMatch, AdminAnnouncement):
	admin.site.register(model, FriendlyModelAdmin)
