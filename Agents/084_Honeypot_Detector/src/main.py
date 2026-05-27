import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import psutil # pip install psutil
import subprocess
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Honeypot_Detector:
    def __init__(self):
        self.agent_id = "77"
        self.name = "Honeypot_Detector"
        self.db = ChimeraDB()
        self.suspicion_score = 0

    def check_processes(self):
        """Honeypots often have very few running processes."""
        proc_count = len(psutil.pids())
        if proc_count < 50:
            self.suspicion_score += 30
            self.logger.warning(f"[!] Low process count detected: {proc_count}")

    def check_history(self):
        """Real systems have long, messy bash histories."""
        history_file = os.path.expanduser("~/.bash_history")
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                lines = f.readlines()
                if len(lines) < 10:
                    self.suspicion_score += 20
        else:
            self.suspicion_score += 40 # No history at all is very sus

    def check_mac_address(self):
        """Check for common VM/Honeypot MAC prefixes (e.g., 08:00:27 is VirtualBox)."""
        try:
            result = subprocess.run(["ip", "link"], capture_output=True, text=True)
            if "08:00:27" in result.stdout or "00:05:69" in result.stdout:
                self.suspicion_score += 20
        except:
            pass

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        
        self.check_processes()
        self.check_history()
        self.check_mac_address()
        
        status = "DANGEROUS" if self.suspicion_score > 50 else "LIKELY_REAL"
        
        self.db.report_finding(self.name, "Honeypot_Analysis_Complete", {
            "score": self.suspicion_score,
            "verdict": status
        })
        
        if status == "DANGEROUS":
            print(f"\n{self.name} WARNING: High probability of Honeypot! Score: {self.suspicion_score}")
        
        self.db.close()

if __name__ == "__main__":
    # Requires: pip install psutil
    agent = Honeypot_Detector()
    agent.run()
