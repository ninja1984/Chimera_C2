import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import re
import logging

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Secret_Scanner:
    def __init__(self):
        self.agent_id = "34"
        self.name = "Secret_Scanner"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.StreamHandler())

        # Regex patterns for common "Golden Nuggets"
        self.patterns = {
            "SSH_Private_Key": r"-----BEGIN (RSA|OPENSSH|DSA|EC) PRIVATE KEY-----",
            "Generic_Password": r"(?i)(password|passwd|pwd|secret|auth)\s*[:=]\s*['\"]([^'\"]+)['\"]",
            "AWS_Key": r"AKIA[0-9A-Z]{16}",
            "Environment_Var": r"(DB_PASSWORD|API_KEY|SECRET_KEY|JDBC_URL)\s*="
        }

    def scan_file(self, file_path):
        """Scans a single file for sensitive patterns."""
        try:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                for secret_type, pattern in self.patterns.items():
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        self.logger.warning(f"[!!!] {secret_type} FOUND in {file_path}")
                        self.db.report_finding(self.name, "Sensitive_Secret", {
                            "type": secret_type,
                            "file": file_path,
                            "snippet": match.group(0)[:50] # Send first 50 chars for verification
                        })
        except Exception as e:
            self.logger.error(f"Failed to scan {file_path}: {e}")

    def run(self):
        self.db.heartbeat(self.name)
        # Scan the 'loot' directory where other agents dump files
        loot_path = "/home/dan/Chimera_Project/loot"
        if not os.path.exists(loot_path):
            self.logger.info("Loot directory empty. Nothing to scan yet.")
            return

        for root, dirs, files in os.walk(loot_path):
            for file in files:
                full_path = os.path.join(root, file)
                self.scan_file(full_path)
        
        self.db.close()

if __name__ == "__main__":
    agent = Secret_Scanner()
    agent.run()
