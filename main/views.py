from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from ArkServer.utility import get_server_info
from django.views.decorators.csrf import csrf_exempt

import json

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from .models import ServerConfigRequest


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


def admin_messages(request):
    from .models import AdminAnnouncement
    announcements = AdminAnnouncement.objects.all().order_by('-created_at')
    data = [{'message': a.message, 'created_at': a.created_at} for a in announcements]
    return JsonResponse(data, safe=False)

def build_ini_strings(payload):
    """Helper to compile GameUserSettings.ini and Game.ini from the JSON payload."""
    rates = payload.get('rates', {})
    breeding = payload.get('breeding', {})
    qol = payload.get('qol', {})
    stats = payload.get('stats', {})

    max_dino_lvl = int(rates.get('max_wild_level', 150))
    official_diff = round(max_dino_lvl / 30.0, 2)

    gus_lines = [
        "[ServerSettings]",
        f"DifficultyOffset=1.0",
        f"OverrideOfficialDifficulty={official_diff}",
        f"XPMultiplier={rates.get('xp', 1.0)}",
        f"TamingSpeedMultiplier={rates.get('taming', 1.0)}",
        f"HarvestAmountMultiplier={rates.get('harvest', 1.0)}",
        f"HarvestHealthMultiplier={rates.get('harvest_health', 1.0)}",
        f"ResourcesRespawnPeriodMultiplier={rates.get('resource_respawn', 1.0)}",
        f"PassiveTameIntervalMultiplier={rates.get('passive_tame_interval', 1.0)}",
        f"ItemStackSizeMultiplier={qol.get('stack_size', 1.0)}",
        f"AllowFlyerCarryPvE={str(qol.get('allow_flyer_carry', True)).lower()}",
        f"AllowFlyerSpeedLeveling={str(qol.get('allow_flyer_speed', False)).lower()}",
        f"AllowSpeedLeveling={str(qol.get('allow_speed_leveling', False)).lower()}",
        f"ShowFloatingDamageText={str(qol.get('floating_damage', True)).lower()}",
        f"AllowAnyoneBabyImprintCuddle={str(breeding.get('anyone_can_imprint', True)).lower()}",
        f"DisableImprintDinoBuff={str(breeding.get('disable_imprint_buff', False)).lower()}",
    ]

    if payload.get('visibility') == 'private' and payload.get('server_password'):
        gus_lines.append(f"ServerPassword={payload.get('server_password')}")

    game_lines = [
        "[/Script/ShooterGame.ShooterGameMode]",
        f"MatingIntervalMultiplier={breeding.get('mating_interval', 1.0)}",
        f"EggHatchSpeedMultiplier={breeding.get('egg_hatch_speed', 1.0)}",
        f"BabyMatureSpeedMultiplier={breeding.get('baby_mature_speed', 1.0)}",
        f"BabyCuddleIntervalMultiplier={breeding.get('cuddle_interval', 1.0)}",
        f"BabyImprintAmountMultiplier={breeding.get('imprint_amount', 1.0)}",
        f"BabyFoodConsumptionSpeedMultiplier={breeding.get('baby_food_consumption', 1.0)}",
    ]

    # Map Per-Level Stats (Indices 0 through 11)
    # 0:Health, 1:Stamina, 2:Torpidity, 3:Oxygen, 4:Food, 5:Water, 6:Temp, 7:Weight, 8:Melee, 9:Speed, 10:Fortitude, 11:Crafting
    for group_key, ini_key in [
        ('player', 'PerLevelStatsMultiplier_Player'),
        ('tamed', 'PerLevelStatsMultiplier_DinoTamed'),
        ('wild', 'PerLevelStatsMultiplier_DinoWild'),
    ]:
        stat_dict = stats.get(group_key, {})
        for idx, val in stat_dict.items():
            if float(val) != 1.0:
                game_lines.append(f"{ini_key}[{idx}]={val}")

    return "\n".join(gus_lines), "\n".join(game_lines)


def server_builder_page(request):
    """Renders the HTML page containing the ARK intake form."""
    return render(request, 'main/build_requests.html')


@require_http_methods(["POST"])
def submit_server_config(request):
    """API endpoint that accepts the JSON payload from the frontend form."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload.'}, status=400)

    server_name = data.get('server_name', '').strip()
    requester_name = data.get('requester_name', '').strip()

    if not server_name or not requester_name:
        return JsonResponse(
            {'status': 'error', 'message': 'Server Name and Requester Name/Discord are required.'},
            status=400
        )

    # Compile INI strings on the server or use client-supplied preview
    gus_ini, game_ini = build_ini_strings(data)

    config_obj = ServerConfigRequest.objects.create(
        requester_name=requester_name,
        server_name=server_name,
        game_version=data.get('game_version', 'ASA'),
        visibility=data.get('visibility', 'public'),
        server_password=data.get('server_password', ''),
        maps=data.get('maps', []),
        mods_requested=data.get('mods_requested', ''),
        blacklisted_items=data.get('blacklisted_items', ''),
        custom_notes=data.get('custom_notes', ''),
        config_payload=data,
        game_user_settings_ini=data.get('raw_gus_ini') or gus_ini,
        game_ini=data.get('raw_game_ini') or game_ini,
    )

    return JsonResponse({
        'status': 'success',
        'request_id': config_obj.id,
        'message': f'Configuration for "{config_obj.server_name}" saved! Ready for Beacon import.'
    })


@staff_member_required
def export_beacon_spec(request, pk):
    """Staff-only view to download a combined INI/Beacon spec sheet from the admin."""
    config = get_object_or_404(ServerConfigRequest, pk=pk)
    content = (
        f"# ==========================================\n"
        f"# BEACON BUILD SPEC: {config.server_name} ({config.game_version})\n"
        f"# Requested By: {config.requester_name}\n"
        f"# Maps: {', '.join(config.maps)}\n"
        f"# ==========================================\n\n"
        f"# --- MODS REQUESTED ---\n{config.mods_requested or 'None'}\n\n"
        f"# --- BLACKLISTED ITEMS / ENGRAMS ---\n{config.blacklisted_items or 'None'}\n\n"
        f"# --- EXTRA NOTES / LOOT DROPS ---\n{config.custom_notes or 'None'}\n\n"
        f"# ==========================================\n"
        f"# GameUserSettings.ini\n"
        f"# ==========================================\n"
        f"{config.game_user_settings_ini}\n\n"
        f"# ==========================================\n"
        f"# Game.ini\n"
        f"# ==========================================\n"
        f"{config.game_ini}\n"
    )
    response = HttpResponse(content, content_type='text/plain')
    safe_name = "".join(c if c.isalnum() else "_" for c in config.server_name)
    response['Content-Disposition'] = f'attachment; filename="Beacon_Spec_{safe_name}.ini"'
    return response