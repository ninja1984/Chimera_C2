#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def sync_all_loot():
    print("[*] [Agent 212] Shadow-Sync: Compiling Master Intelligence Report...")
    
    # Pathing
    agents_dir = "/home/dan/Chimera_Project/agents"
    master_loot_file = os.path.join(agents_dir, "212_Shadow_Sync", "loot", "MASTER_REPORT.txt")
    
    report_content = []
    report_content.append(f"=== CHIMERA PROJECT MASTER REPORT ===")
    report_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append("="*40 + "\n")

    # Iterate through all agent directories
    for agent_folder in sorted(os.listdir(agents_dir)):
        loot_dir = os.path.join(agents_dir, agent_folder, "loot")
        
        if os.path.exists(loot_dir):
            for loot_file in os.listdir(loot_dir):
                file_path = os.path.join(loot_dir, loot_file)
                # Don't include the master report in itself
                if "MASTER_REPORT" in loot_file: continue
                
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        data = f.read().strip()
                        if data:
                            report_content.append(f"--- AGENT: {agent_folder} | FILE: {loot_file} ---")
                            report_content.append(data)
                            report_content.append("-" * 20 + "\n")
                except Exception:
                    continue

    with open(master_loot_file, "w") as f:
        f.write("\n".join(report_content))

    print(f"[+] Master Sync Complete! All intelligence consolidated to: {master_loot_file}")

if __name__ == "__main__":
    sync_all_loot()
