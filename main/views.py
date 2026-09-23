from django.shortcuts import render
from django.http import HttpResponse
from ArkServer.utility import get_server_info

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

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
    rag_info = get_server_info("DDD_RAG_ID")
    print(f"RAG Info: {rag_info}")
    isl_info = get_server_info("DDD_ISL_ID")
    print(f"ISL Info: {isl_info}")
    ast_info = get_server_info("DDD_AST_ID")
    print(f"AST Info: {ast_info}")
    total_players = rag_info['player_current'] + isl_info['player_current'] + ast_info['player_current']

    return render(request, 'main/server_stats/dodo_domain_stats.html', {
        'rag_info': rag_info,
        'isl_info': isl_info,
        'ast_info': ast_info,
        'total_players': total_players,
    })

