from django.contrib import admin
from django.urls import path
from .views import home, update_dodoball, dodo_domain_stats

urlpatterns = [
    path('', home, name='home'),
    path('servers/dodo_domain/', dodo_domain_stats, name='dodo_domain_stats'),
    path('update_dodoball/', update_dodoball, name='update_dodoball'), 

]