#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import sys
import os
import re
import json
from datetime import datetime

class EmailHarvester:
    """
    Agent 14: Passive Identity Harvester.
    Scrapes public PGP keyservers to identify valid internal email addresses
    and corporate naming conventions without direct target contact.
    """
    def __init__(self, domain):
        self.domain = domain
        self.loot_dir = "/home/dan/Chimera_Project/agents/14_Email_Harvester/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.found_emails = set()

    def scrape_pgp_keyservers(self):
        """Queries MIT PGP Public Keyserver for domain-linked UIDs."""
        print(f"[*] AGENT 14: Scraping PGP Keyservers for @{self.domain}...")
        url = f"https://pgp.mit.edu/pks/lookup?search={self.domain}&op=index"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # Regex to extract email patterns from the HTML response
                pattern = r'[a-zA-Z0-9._%+-]+@' + re.escape(self.domain)
                emails = re.findall(pattern, r.text)
                for email in emails:
                    self.found_emails.add(email.lower())
        except Exception as e:
            print(f"    [!] Keyserver Scraping Failed: {e}")

    def execute(self):
        print(f"--- [AGENT 14: EMAIL HARVESTING - {self.domain}] ---")
        self.scrape_pgp_keyservers()
        
        if self.found_emails:
            print(f"[+] Discovered {len(self.found_emails)} unique internal addresses.")
            for email in sorted(list(self.found_emails)):
                print(f"    [>] {email}")
            
            # Commit to Loot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/emails_{self.domain}_{timestamp}.json"
            
            payload = {
                "timestamp": str(datetime.now()),
                "domain": self.domain,
                "count": len(self.found_emails),
                "emails": list(self.found_emails)
            }
            
            with open(loot_file, 'w') as f:
                json.dump(payload, f, indent=4)
                
            print(f"[!!!] IDENTITY INTELLIGENCE COMMITTED: {loot_file}")
            return payload
        else:
            print("[-] No public email records discovered.")
            return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_domain>")
        sys.exit(1)
        
    EmailHarvester(sys.argv[1]).execute()
