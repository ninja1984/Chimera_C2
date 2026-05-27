import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import shutil
import subprocess
import logging

# Ensure the agent can find the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Self_Destruct_Protocol:
    def __init__(self):
        self.agent_id = "42"
        self.name = "Self_Destruct"
        self.db = ChimeraDB()
        self.project_root = "/home/dan/Chimera_Project"

    def wipe_footprints(self):
        """Kills all processes, wipes logs, and deletes the loot."""
        print("[!!!] INITIALIZING SELF-DESTRUCT PROTOCOL...")
        
        try:
            # 1. Kill all Python processes related to Chimera
            subprocess.run(["pkill", "-f", "Chimera_Project"], capture_output=True)
            
            # 2. Wipe the Loot and Logs
            loot_dir = os.path.join(self.project_root, "loot")
            log_dir = os.path.join(self.project_root, "logs")
            
            if os.path.exists(loot_dir):
                shutil.rmtree(loot_dir)
                os.makedirs(loot_dir) # Keep the folder but empty
                
            if os.path.exists(log_dir):
                for f in os.listdir(log_dir):
                    os.remove(os.path.join(log_dir, f))
            
            # 3. Wipe Shell History (The 'Anti-Forensics' special)
            subprocess.run(["history", "-c"], shell=True)
            
            print("[+] Footprints sanitized. Chimera is now a ghost.")
            
        except Exception as e:
            print(f"[-] Self-destruct partial failure: {e}")

    def run(self):
        self.wipe_footprints()
        self.db.close()

if __name__ == "__main__":
    agent = Self_Destruct_Protocol()
    agent.run()
