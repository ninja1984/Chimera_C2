#!/usr/bin/env python3
import os
import sys
import tarfile
from datetime import datetime

def omega_finalize(target_id):
    print(f"[*] [Agent 187] Omega Finalizer: Aggregating all Chimera data for: {target_id}")
    
    # Define paths relative to this script's location
    # Structure: /home/dan/Chimera_Project/agents/187_Omega_Finalizer/src/main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agents_root = os.path.dirname(os.path.dirname(current_dir)) # Hits /agents/
    
    loot_dir = os.path.join(os.path.dirname(current_dir), "loot")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_name = os.path.join(loot_dir, f"CHIMERA_FINAL_{target_id}_{timestamp}.tar.gz")

    if not os.path.exists(loot_dir):
        os.makedirs(loot_dir)

    print(f"[*] Scanning {agents_root} for agent loot...")
    
    try:
        with tarfile.open(archive_name, "w:gz") as tar:
            # Walk through every agent directory (01 through 200)
            for item in os.listdir(agents_root):
                agent_path = os.path.join(agents_root, item)
                
                # Check if it's an agent folder and has a loot directory
                if os.path.isdir(agent_path):
                    specific_loot_path = os.path.join(agent_path, "loot")
                    
                    if os.path.exists(specific_loot_path) and os.listdir(specific_loot_path):
                        print(f"[+] Adding loot from: {item}")
                        # Add to archive, renaming internal folder for clarity
                        tar.add(specific_loot_path, arcname=f"{item}_loot")
        
        if os.path.exists(archive_name):
            print(f"\n[SUCCESS] Final Intelligence Package: {archive_name}")
        else:
            print("[!] Warning: No loot found to archive.")
            
    except Exception as e:
        print(f"[!] Critical Finalization Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_name_or_ip>")
        sys.exit(1)
    
    omega_finalize(sys.argv[1])
