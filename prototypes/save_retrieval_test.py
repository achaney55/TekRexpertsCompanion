import ftplib
import json
import os
import ssl
import tempfile
from arkparser import Profile, WorldSave, export_all, export_to_files
from arkparser.common import get_map_config
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

print(f"FTP_HOST: {FTP_HOST}")

class ImplicitFTP_TLS(ftplib.FTP_TLS):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssl_version = ssl.PROTOCOL_TLSv1_2


def inspect_embedded_save_data():
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
        linked_id = getattr(first_player_pawn.get_property("LinkedPlayerDataID"), "_value", None) if first_player_pawn else None
        player = first_player_pawn.get_property("Player") if first_player_pawn else None
        character_name = getattr(first_player_pawn.get_property("PlayerName"), "_value", None) if first_player_pawn else None
        platform_profile_name = getattr(first_player_pawn.get_property("PlatformProfileName"), "_value", None) if first_player_pawn else None
        tribe_name = getattr(first_player_pawn.get_property("TribeName"), "_value", None) if first_player_pawn else None
        is_sleeping = getattr(first_player_pawn.get_property("bIsSleeping"), "_value", None) if first_player_pawn else None
        print("\nLinkedPlayerDataID:", linked_id)
        
        print("\nCharacter Name:", character_name)
        
        print("\nPlatform Profile Name:", platform_profile_name)

        print("\nTribe Name:", tribe_name)
        print("\nIs Sleeping:", str(is_sleeping))
    
    except Exception as e:
        print(f"Error parsing .ark world file: {e}")
    finally:
        if os.path.exists(temp_save_path):
            os.remove(temp_save_path)


if __name__ == "__main__":
    inspect_embedded_save_data()