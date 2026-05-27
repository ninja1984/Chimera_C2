import os
import sys
import shutil
from datetime import datetime

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[32m" + "="*60)
    print("   CHIMERA AGENT 34 :: TARGET ARCHIVER & LOOT MANAGER")
    print("="*60 + "\033[0m")

    target = input("[?] Target IP or Domain to Archive: ").strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Define paths
    loot_dir = "/home/dan/Chimera_Project/loot"
    archive_dir = f"/home/dan/Chimera_Project/archives/{target}_{timestamp}"

    if not os.path.exists(loot_dir):
        print("[!] No loot directory found. Nothing to archive.")
        return

    print(f"[*] Creating archive for {target} at {archive_dir}...")

    try:
        # 1. Create the archive directory
        os.makedirs(archive_dir, exist_ok=True)

        # 2. Move target-specific files from loot to archive
        # (Assuming you named your files/folders by target IP/Domain)
        moved_count = 0
        for item in os.listdir(loot_dir):
            if target in item:
                shutil.move(os.path.join(loot_dir, item), archive_dir)
                moved_count += 1
        
        print(f"\033[92m[+] Successfully archived {moved_count} items.\033[0m")
        
        db.report_finding("34_Target_Archiver", "Target_Archived", {
            "target": target,
            "archive_path": archive_dir,
            "items_moved": moved_count
        })

    except Exception as e:
        print(f"\033[91m[!] Archiving failed: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
