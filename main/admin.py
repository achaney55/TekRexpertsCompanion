from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import PlayerProfile, Tribe, Creature, DodoBallMatch, AdminAnnouncement, ServerConfigRequest

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


@admin.register(ServerConfigRequest)
class ServerConfigRequestAdmin(admin.ModelAdmin):
    list_display = (
        'server_name',
        'requester_name',
        'game_version',
        'visibility',
        'status',
        'created_at',
        'download_spec_button',
    )
    list_filter = ('status', 'game_version', 'visibility', 'created_at')
    search_fields = ('server_name', 'requester_name', 'mods_requested', 'blacklisted_items')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Overview & Status', {
            'fields': ('status', 'server_name', 'requester_name', 'game_version', 'visibility', 'server_password')
        }),
        ('Cluster & Customization', {
            'fields': ('maps', 'mods_requested', 'blacklisted_items', 'custom_notes')
        }),
        ('Generated INI Blocks (Copy into Beacon)', {
            'fields': ('game_user_settings_ini', 'game_ini'),
        }),
        ('Raw JSON Payload', {
            'classes': ('collapse',),
            'fields': ('config_payload', 'created_at', 'updated_at'),
        }),
    )

    def download_spec_button(self, obj):
        url = reverse('ark_builder:export_beacon_spec', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="padding:4px 8px; background:#0ea5e9; color:#fff; border-radius:4px; text-decoration:none;">Download .INI</a>',
            url
        )
    download_spec_button.short_description = 'Beacon Spec'