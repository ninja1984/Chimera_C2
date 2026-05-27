#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import sys
import os
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class CloudStorageFinder:
    """
    Agent 13: Public Cloud Bucket Enumerator.
    Permutes the target domain into common AWS/Azure/GCP bucket formats
    and probes for existence and access permissions.
    """
    def __init__(self, domain):
        self.domain = domain.split('.')[0]
        self.loot_dir = "/home/dan/Chimera_Project/agents/13_Cloud_Storage_Finder/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        
        self.suffixes = [
            "backup", "data", "prod", "dev", "staging", 
            "logs", "sql", "archive", "test", "web", "assets"
        ]
        self.found_buckets = []

    def _probe_s3(self, name):
        """Probes Amazon S3 infrastructure."""
        url = f"https://{name}.s3.amazonaws.com"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 404:
                status = "OPEN" if r.status_code == 200 else "SECURED (403)"
                res = f"[S3] {url} - {status}"
                print(f"    [!] {res}")
                return res
        except: pass
        return None

    def execute(self, threads=10):
        print(f"--- [AGENT 13: CLOUD STORAGE ENUMERATION - {self.domain}] ---")
        
        # Generate permutation list
        names = [self.domain]
        for s in self.suffixes:
            names.append(f"{self.domain}-{s}")
            names.append(f"{self.domain}{s}")
            names.append(f"{s}-{self.domain}")

        print(f"[*] Probing {len(names)} bucket permutations...")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = executor.map(self._probe_s3, names)
            for r in results:
                if r:
                    self.found_buckets.append(r)

        # Intelligence Commitment
        if self.found_buckets:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/buckets_{self.domain}_{timestamp}.json"
            
            with open(loot_file, 'w') as f:
                json.dump({
                    "target": self.domain,
                    "buckets": self.found_buckets
                }, f, indent=4)
            
            print(f"[!!!] CLOUD INTELLIGENCE COMMITTED: {loot_file}")
        else:
            print("[-] No public cloud buckets identified.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_domain_prefix>")
        sys.exit(1)
        
    CloudStorageFinder(sys.argv[1]).execute()
