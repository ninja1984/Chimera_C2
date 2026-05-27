#!/home/dan/Chimera_Project/venv/bin/python3
import sys
import os
import json
import re
from datetime import datetime

class VulnScannerPro:
    """
    Agent 108 Pro: Dynamic Vulnerability Correlation.
    Parses banners against an external JSON-fed database to allow 
    for 0-day updates without modifying agent code.
    """
    def __init__(self, target):
        self.target = target
        self.db_path = "/home/dan/Chimera_Project/agents/108_Vuln_Scanner/db/vuln_feed.json"
        self.loot_dir = "/home/dan/Chimera_Project/agents/108_Vuln_Scanner/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        
        # Load the dynamic feed
        with open(self.db_path, 'r') as f:
            self.vuln_data = json.load(f)

    def search_vulns(self, banner):
        """Dynamic searching using regex and key-matching."""
        findings = []
        banner_lower = banner.lower()
        
        # Iterate through the dynamic service categories (ssh, apache, etc.)
        for service, versions in self.vuln_data.items():
            if service in banner_lower:
                for version, cves in versions.items():
                    if version in banner_lower:
                        for cve in cves:
                            findings.append({"service": service, "ver": version, "cve": cve})
        return findings

    def execute(self, banner_loot_path):
        print(f"--- [AGENT 108: DYNAMIC VULN SCAN - {self.target}] ---")
        
        if not os.path.exists(banner_loot_path):
            print("[!] Error: No banner intelligence found for target.")
            return

        with open(banner_loot_path, 'r') as f:
            banners = json.load(f).get("banners", {})

        all_matches = []
        for port, banner in banners.items():
            print(f"[*] Analyzing Port {port}: {banner[:40]}...")
            matches = self.search_vulns(banner)
            if matches:
                for m in matches:
                    print(f"    [!!!] POTENTIAL EXPLOIT: {m['cve']} ({m['service']} {m['ver']})")
                    all_matches.append({"port": port, "vuln": m['cve']})

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/vulns_{self.target}_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump({"target": self.target, "matches": all_matches}, f, indent=4)
        
        print(f"[!!!] VULNERABILITY MAP COMMITTED: {loot_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    target = sys.argv[1]
    banner_file = sys.argv[2]
    VulnScannerPro(target).execute(banner_file)
