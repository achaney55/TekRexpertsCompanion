import ftplib
import os
import ssl
import tempfile
from arkparser import Profile, WorldSave, export_all, export_to_files
from arkparser.common import get_map_config
import requests
from pathlib import Path
from dotenv import load_dotenv

# Option B (Most reliable): Pin the path relative to this script file
# Useful if running the script from a subfolder like /prototypes/
script_dir = Path(__file__).resolve().parent
# If .env is in the project root, step up as needed:
env_path = script_dir.parent / ".env"  # or script_dir / ".env"
load_dotenv(dotenv_path=env_path)

env = os.environ

FTP_HOST = env.get("FTP_HOST")
FTP_PORT = int(env.get("FTP_PORT", 21))
FTP_USER = env.get("FTP_USER")
FTP_PASS = env.get("FTP_PASS")
REMOTE_SAVE_DIR = env.get("REMOTE_SAVE_DIR")
WORLD_SAVE_FILE = "TheIsland_WP.ark"

class ImplicitFTP_TLS(ftplib.FTP_TLS):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssl_version = ssl.PROTOCOL_TLSv1_2

def sync_world_save():
    ftps = ImplicitFTP_TLS()
    print("Connecting to Nitrado...")
    ftps.connect(FTP_HOST, FTP_PORT, timeout=30)
    ftps.login(FTP_USER, FTP_PASS)
    ftps.prot_p()
    ftps.cwd(REMOTE_SAVE_DIR)

    # 1. Stream the .ark file to a temporary file
    # Note: ASA .ark files can be 100MB - 1GB+ depending on days running
    print(f"Downloading {WORLD_SAVE_FILE}...")
    with tempfile.NamedTemporaryFile(suffix=".ark", delete=False) as tmp:
        temp_save_path = tmp.name
        ftps.retrbinary(f"RETR {WORLD_SAVE_FILE}", tmp.write)

    ftps.quit()
    print("Download complete. Parsing world save...")

    try:
        # 2. Parse the container
        save = WorldSave.load(temp_save_path)

        # Load map calibration for ASA The Island
        map_config = get_map_config("TheIsland_WP.ark")

        
        # Extract everything into native Python dictionaries
        game_data = export_to_files(save, "output/", map_config)
        player_pawns = save.get_player_pawns()  # Should show keys like 'ASV_Players', 'ASV_Tamed', 'ASV_Tribes'

        #Navigate player pawns python object to get the LinkedPlayerDataID and PlatformNetId for a specific player
        # Example: Get the first player pawn's LinkedPlayerDataID and PlatformNetId
        first_player_pawn = player_pawns[0] if player_pawns else None
        linked_id = first_player_pawn.get_property("LinkedPlayerDataID") if first_player_pawn else None
        linked_id = getattr(first_player_pawn.get_property("LinkedPlayerDataID"), "_value", None) if first_player_pawn else None
        platform_net_id = first_player_pawn.get_property("PlatformNetId") if first_player_pawn else None

        print("LinkedPlayerDataID:", linked_id)
        # Output: 734832255     
        
        print("Platform Net ID:", platform_net_id)
        # Output: 0002b5e30ce04450bf8e0ae72c23cee2
        
    except Exception as e:
        print(f"Error parsing .ark world file: {e}")

    finally:
        if os.path.exists(temp_save_path):
            os.remove(temp_save_path)


def get_server_info(service_id_name):
    NITRADO_TOKEN = env.get("NITRADO_TOKEN")
    SERVICE_ID = env.get(service_id_name)

    url = f"https://api.nitrado.net/services/{SERVICE_ID}/gameservers"

    headers = {
        "Authorization": f"Bearer {NITRADO_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        gameserver = data.get("data", {}).get("gameserver", {})
        
        # Common statuses: 'started', 'stopped', 'restarting', 'suspended'
        status = gameserver.get("status")
        game = gameserver.get("game_human")
        query_info = gameserver.get("query", {})
        
        print(f"Game: {game}")
        print(f"Status: {status}")
        print(f"Is Online: {status == 'started'}")
        
        # If the server is online and responding to query:
        if query_info:
            player_current = query_info.get("player_current", 0)
            player_max = query_info.get("player_max", 0)
            server_name = query_info.get("server_name")
            print(f"Server Name: {server_name}")
            print(f"Players: {player_current}/{player_max}")

            #Extract map name after first '-' and before second '-'
            map_name = None
            if server_name:
                parts = server_name.split('-')
                if len(parts) >= 3:
                    map_name = parts[1]
            print(f"Map Name: {map_name}")
            #remove empty spaces from map name
            if map_name:
                map_name = map_name.replace(" ", "")
            return {
                "player_current": player_current,
                "player_max": player_max,
                "server_name": server_name,
                "is_online": status == 'started',
                "map_name": map_name
            }
        return {
            "player_current": 0,
            "player_max": 0,
            "server_name": None,
            "is_online": False,
            "map_name": None
        }
    else:
        print(f"Failed to fetch server info. Status code: {response.status_code}")
        return {
            "player_current": 0,
            "player_max": 0,
            "server_name": None,
            "is_online": False,
            "map_name": None
        }
        