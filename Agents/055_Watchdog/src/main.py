import os
import sys
import time
from datetime import datetime

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[94m" + "="*60)
    print("   CHIMERA AGENT 48 :: SWARM WATCHDOG & LOG ANALYZER")
    print("="*60 + "\033[0m")

    log_dir = "/home/dan/Chimera_Project/logs"
    print(f"[*] Monitoring logs in {log_dir}...")

    try:
        while True:
            # 1. Check for Active Beacons in Neo4j
            # (Logic: If a target hasn't checked in for 5 minutes, mark as STALE)
            active_targets = db.get_active_beacons() # Assuming this method exists in your DB handler
            
            # 2. Monitor Log Files for 'CRITICAL' errors
            for log_file in os.listdir(log_dir):
                full_path = os.path.join(log_dir, log_file)
                with open(full_path, 'r') as f:
                    # Check last 10 lines for crashes
                    lines = f.readlines()[-10:]
                    for line in lines:
                        if "CRITICAL" in line or "Traceback" in line:
                            print(f"\033[91m[!] ALERT: Agent Failure Detected in {log_file}\033[0m")
                            # In an autonomous setup, you'd trigger a restart command here:
                            # os.system(f"python3 agents/{log_file.replace('.log', '')}/src/main.py &")

            # 3. Check Disk Space (Essential for long-running loot harvesting)
            stat = os.statvfs('/home/dan/Chimera_Project/loot')
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            if free_gb < 1.0:
                print("\033[93m[!] WARNING: Low Disk Space for Loot (< 1GB)!\033[0m")

            time.sleep(60) # Run check every minute

    except KeyboardInterrupt:
        print("\n[*] Watchdog suspended.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
