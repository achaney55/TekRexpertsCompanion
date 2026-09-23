from django.contrib import admin
from django.urls import path
from .views import home, update_dodoball, dodo_domain_stats, gbr_stats, dodo_domain_maps

urlpatterns = [
    path('', home, name='home'),
    path('servers/dodo_domain/', dodo_domain_stats, name='dodo_domain_stats'),
    path('api/maps/dodo_domain/', dodo_domain_maps, name='api_dodo_domain_maps'),
    path('servers/gigabite_retreat/', gbr_stats, name='gbr_stats'),
    path('update_dodoball/', update_dodoball, name='update_dodoball'), 

]