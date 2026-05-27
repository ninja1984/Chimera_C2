#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import socket
import sys
import os
import json
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class SubdomainScanner:
    """
    Agent 02: Subdomain Discovery Engine.
    Combines Passive CT Log Scraping with Active Multi-Threaded DNS Resolution.
    Designed for stealthy surface mapping prior to active port scanning.
    """
    def __init__(self, domain):
        self.domain = domain
        self.loot_dir = f"/home/dan/Chimera_Project/agents/02_Subdomain_Scanner/loot/{self.domain}"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.candidates = set()
        self.live_map = {}

    def passive_harvest_ct(self):
        """
        Queries Certificate Transparency logs (crt.sh).
        This is 100% passive; no packets are sent to the target's network.
        """
        print(f"[*] AGENT 02: Harvesting CT Logs for {self.domain} (Passive Phase)...")
        url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
        try:
            # Using a long timeout for crt.sh's often slow database
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    # Clean and split potentially multiple subdomains in one entry
                    names = entry['name_value'].split('\n')
                    for name in names:
                        clean_name = name.replace('*.', '').lower().strip()
                        if clean_name.endswith(self.domain):
                            self.candidates.add(clean_name)
                print(f"[+] Passive Harvest Complete: {len(self.candidates)} candidates identified.")
        except Exception as e:
            print(f"[!] Passive Harvest Error: {e}")

    def _resolve_dns(self, subdomain):
        """Performs raw DNS resolution to verify host existence."""
        try:
            # Low-level socket resolution to minimize overhead
            ip = socket.gethostbyname(subdomain)
            self.live_map[subdomain] = ip
            print(f"    [>] LIVE: {subdomain} -> {ip}")
        except (socket.gaierror, socket.timeout):
            pass

    def verify_active_hosts(self, thread_count=20):
        """
        Active Phase: Multi-threaded verification of candidates.
        """
        print(f"[*] AGENT 02: Verifying {len(self.candidates)} candidates via DNS...")
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            executor.map(self._resolve_dns, sorted(list(self.candidates)))

    def execute(self):
        print(f"--- [AGENT 02: SUBDOMAIN DISCOVERY - {self.domain}] ---")
        
        # 1. Passive Phase
        self.passive_harvest_ct()
        
        # 2. Active Phase
        if self.candidates:
            self.verify_active_hosts()
            
            # 3. Intelligence Storage
            if self.live_map:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"{self.loot_dir}/map_{timestamp}.json"
                with open(output_file, 'w') as f:
                    json.dump(self.live_map, f, indent=4)
                print(f"[!!!] RECON COMPLETE: {len(self.live_map)} live hosts committed to {output_file}")
                return output_file
        
        print("[-] No actionable intelligence gathered.")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_domain>")
        sys.exit(1)
        
    target = sys.argv[1]
    SubdomainScanner(target).execute()
