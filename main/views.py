from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def update_dodoball(request):
    from .models import DodoBallMatch
    pointsToAdd = request.GET.get('pointsToAdd')
    # Add logic to update DodoBall status for the given net_id
    print(f"Team scored points in dodoball: {pointsToAdd}")
    return HttpResponse(f"Points to add: {pointsToAdd}")

def dodo_domain_stats(request):
    return render(request, 'main/server_stats/dodo_domain_stats.html')

def gbr_stats(request):
    return render(request, 'main/server_stats/gbr_stats.html')