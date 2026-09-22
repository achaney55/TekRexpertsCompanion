from django.contrib import admin
from django.urls import path
from .views import home, update_dodoball

urlpatterns = [
    path('', home, name='home'),
    path('update_dodoball/', update_dodoball, name='update_dodoball'), 

]