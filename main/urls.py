from django.contrib import admin
from django.urls import path
from .views import admin_messages, home, update_dodoball, dodo_domain_stats, gbr_stats, dodo_domain_maps, server_builder_page, submit_server_config, export_beacon_spec

urlpatterns = [
    path('', home, name='home'),
    path('servers/dodo_domain/', dodo_domain_stats, name='dodo_domain_stats'),
    path('api/maps/dodo_domain/', dodo_domain_maps, name='api_dodo_domain_maps'),
    path('servers/gigabite_retreat/', gbr_stats, name='gbr_stats'),
    path('update_dodoball/', update_dodoball, name='update_dodoball'), 
    path('api/messages/admin/', admin_messages, name='api_admin_messages'),
    path('request-server/', server_builder_page, name='builder_page'),
    path('api/submit-config/', submit_server_config, name='submit_config'),
    path('admin/export-spec/<int:pk>/', export_beacon_spec, name='export_beacon_spec'),

]