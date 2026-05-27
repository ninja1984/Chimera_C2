import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class SNMP_Walker:
    def __init__(self):
        self.agent_id = "44"
        self.name = "SNMP_Walker"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def walk(self, target_ip, community="public"):
        """Uses snmpwalk to gather system information."""
        self.logger.info(f"Walking SNMP tree on {target_ip} with community '{community}'...")
        
        try:
            # -v2c: Version 2c
            # -c: Community string
            cmd = ["snmpwalk", "-v2c", "-c", community, target_ip]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                # We look for specific interesting strings like 'Software', 'User', or 'Pass'
                lines = result.stdout.splitlines()
                self.logger.info(f"[+] Retrieved {len(lines)} SNMP records.")
                
                # Save a snippet of the most important info to Neo4j
                self.db.report_finding(self.name, "SNMP_Data_Leak", {
                    "ip": target_ip,
                    "community": community,
                    "record_count": len(lines),
                    "system_description": lines[0] if lines else "Unknown"
                })
        except Exception as e:
            self.logger.error(f"SNMP walk failed for {target_ip}: {e}")

    def run(self):
        self.db.heartbeat(self.name)
        # In the swarm, this triggers if Network_Mapper finds Port 161 (SNMP) open
        # self.walk("10.129.6.10")
        self.db.close()

if __name__ == "__main__":
    agent = SNMP_Walker()
    agent.run()
