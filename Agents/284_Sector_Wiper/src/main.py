#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class SectorWiper:
    """
    Agent 429: Physical Evidence Destruction.
    Orchestrates the C-native block-level wiper to 
    neutralize forensic recovery efforts.
    """
    def execute(self, target_path):
        print("--- [AGENT 429: SCORCHED EARTH SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/429_Sector_Wiper/src/wiper.c"
        bin_out = "/home/dan/Chimera_Project/agents/429_Sector_Wiper/src/wiper"
        
        # 1. Compile
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # 2. Wipe
        if os.path.exists(target_path):
            subprocess.run([bin_out, target_path])
        else:
            print(f"[!] Target {target_path} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <file_to_annihilate>")
        sys.exit(1)
    SectorWiper().execute(sys.argv[1])
