import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import requests
import dns.resolver
import logging

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class S3_Bucket_Finder:
    def __init__(self):
        self.agent_id = "15"
        self.name = "S3_Bucket_Finder"
        self.base_dir = "/home/dan/Chimera_Project/agents/S3_Bucket_Finder"
        
        # Setup Logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.StreamHandler())
        
        self.db = ChimeraDB()
        
        # Common suffixes for buckets
        self.suffixes = ['backup', 'dev', 'staging', 'prod', 'logs', 'data', 'sql', 'files']

    def check_bucket(self, bucket_name):
        """
        Probes an S3 URL to see if it exists and if it is public.
        """
        url = f"http://{bucket_name}.s3.amazonaws.com"
        try:
            r = requests.get(url, timeout=5)
            # 200 OK means the bucket is public and listable
            if r.status_code == 200:
                self.logger.info(f"[!!!] PUBLIC BUCKET FOUND: {url}")
                finding_data = {
                    "bucket_url": url,
                    "status": "Public/Listable",
                    "severity": "Critical"
                }
                self.db.report_finding(self.name, "CloudStorage", finding_data)
                return True
            # 403 Forbidden means it exists but is private
            elif r.status_code == 403:
                self.logger.info(f"[+] Private Bucket Found: {url}")
                finding_data = {
                    "bucket_url": url,
                    "status": "Private",
                    "severity": "Info"
                }
                self.db.report_finding(self.name, "CloudStorage", finding_data)
        except Exception:
            pass
        return False

    def generate_permutations(self, target_domain):
        """
        Generates bucket name guesses based on the target domain.
        """
        base = target_domain.split('.')[0]
        names = [base]
        for s in self.suffixes:
            names.append(f"{base}-{s}")
            names.append(f"{base}.{s}")
            names.append(f"{s}-{base}")
        return names

    def run(self):
        self.logger.info(f"{self.name} checking for cloud leaks...")
        self.db.heartbeat(self.name)
        
        # In a real run, this domain would be pulled from the AD_Scout or DNS_Recon findings
        target_domain = "corp.local" 
        
        bucket_guesses = self.generate_permutations(target_domain)
        
        for bucket in bucket_guesses:
            self.check_bucket(bucket)
            
        self.db.close()

if __name__ == "__main__":
    agent = S3_Bucket_Finder()
    agent.run()
