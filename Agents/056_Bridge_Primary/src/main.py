import os
import sys
import json

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[95m" + "="*60)
    print("   CHIMERA AGENT 49 :: BRIDGE_PRIMARY (THE LOGIC GATE)")
    print("="*60 + "\033[0m")

    print("[*] Analyzing Neo4j Graph for actionable intelligence...")

    # 1. Look for un-exploited credentials
    # Logic: If Agent 42 found Joomla creds, but Agent 38 hasn't 'Stuffed' them yet.
    findings = db.get_unprocessed_findings() # Custom query for new nodes

    if not findings:
        print("[*] No new bridging opportunities found. Swarm is idle.")
        return

    for finding in findings:
        target = finding.get('target')
        f_type = finding.get('type')
        
        print(f"\033[92m[+] BRIDGING: {f_type} detected on {target}\033[0m")

        if f_type == "Joomla_API_Exploit_Success":
            print(f"    [!] Logic Trigger: Sending Credentials to Agent 38 (Stuffing)...")
            # In a full auto-run, this would call the subprocess for Agent 38
            # os.system(f"python3 agents/38_Credential_Stuffer/src/main.py --target {target}")

        elif f_type == "Subdomain_Discovered":
            print(f"    [!] Logic Trigger: Mapping new surface via Agent 01...")
            
        elif f_type == "PrivEsc_Vectors_Detected":
            print(f"    [!] Logic Trigger: Passing vector to Agent 18 (Kernel Exploit)...")

    db.close()

if __name__ == "__main__":
    run()
