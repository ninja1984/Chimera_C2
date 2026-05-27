import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import re
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Credential_Digger:
    def __init__(self):
        self.agent_id = "92"
        self.name = "92_Credential_Digger"
        self.db = ChimeraDB()
        self.patterns = {
            "DB_Pass": r"(password|passwd|pwd)\s*[:=]\s*['\"](.*?)['\"]",
            "API_Key": r"(api_key|apikey|secret)\s*[:=]\s*['\"](.*?)['\"]",
            "Connection_Str": r"mongodb\+srv:\/\/|postgres:\/\/|mysql:\/\/"
        }

    def dig(self, search_path="/home/dan/"):
        self.logger.info(f"Scanning {search_path} for secrets...")
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.endswith(('.php', '.js', '.json', '.env', '.conf')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            for p_name, regex in self.patterns.items():
                                matches = re.findall(regex, content, re.IGNORECASE)
                                if matches:
                                    self.db.report_finding(self.name, "Secret_Found", {"file": file_path, "type": p_name})
                    except: continue

    def run(self, path="/home/dan/"):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        self.db.heartbeat(self.name)
        self.dig(path)
        self.db.close()

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "/home/dan/"
    agent = Credential_Digger()
    agent.run(p)
