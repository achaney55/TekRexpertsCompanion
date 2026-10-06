from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from ArkServer.utility import get_server_info
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@csrf_exempt
def dodo_domain_maps(request):
    rag_info = get_server_info("DDD_RAG_ID")
    isl_info = get_server_info("DDD_ISL_ID")
    ast_info = get_server_info("DDD_AST_ID")
    total_players = rag_info['player_current'] + isl_info['player_current'] + ast_info['player_current']

    data = {
        'rag_info': rag_info,
        'isl_info': isl_info,
        'ast_info': ast_info,
        'total_players': total_players,
    }
    return JsonResponse(data)

def update_dodoball(request):
    from .models import DodoBallMatch
    pointsToAdd = request.GET.get('pointsToAdd')
    # Add logic to update DodoBall status for the given net_id
    print(f"Team scored points in dodoball: {pointsToAdd}")
    return HttpResponse(f"Points to add: {pointsToAdd}")

def gbr_stats(request):
    
    return render(request, 'main/server_stats/gbr_stats.html')

def ddd_rag_stats(request):
    server_info = get_server_info("DDD_RAG_ID")
    return render(request, 'main/server_stats/ddd_rag_stats.html')

def ddd_isl_stats(request):
    server_info = get_server_info("DDD_ISL_ID")
    return render(request, 'main/server_stats/ddd_isl_stats.html')

def ddd_ast_stats(request):
    server_info = get_server_info("DDD_AST_ID")
    return render(request, 'main/server_stats/ddd_ast_stats.html')

def dodo_domain_stats(request):
    
    return render(request, 'main/server_stats/dodo_domain_stats.html')

def beacon_login():
    try:
        response = requests.get(
            url="https://api.usebeacon.app/v4/login",
            params={
                "state": "0fc732a9-05d8-403c-bdce-231c90f7b924",
                "client_id": "95e7998f-ae52-4fa2-b0a7-886ff7d43abf",
                "scope": "common users:read",
                "redirect_uri": "https://jiinuko.edu/ehreg/oauth",
                "response_type": "code",
                "code_challenge": "2b6-gW15O10gZcp97PaXVmmu_4IrMXVBXNWtP8q8crs",
                "code_challenge_method": "S256",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')