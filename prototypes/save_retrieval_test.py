import ftplib
import os
import ssl
import tempfile
from arkparser import Profile, WorldSave

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

        # 3. Access embedded player and tribe structures
        print(save.get_player_pawns())
        print(f"Is ASA: {save.is_asa}")
        print(f"Creatures: {save.get_tamed_creatures()}")
        print(f"Players: {save.profiles}")
        print(save.get_object_by_guid("00d42741-3e49-4c47-8a7b-ecbd7766d30c"))  # Example GUID, replace with actual

    except Exception as e:
        print(f"Error parsing .ark world file: {e}")
    finally:
        if os.path.exists(temp_save_path):
            os.remove(temp_save_path)


if __name__ == "__main__":
    inspect_embedded_save_data()