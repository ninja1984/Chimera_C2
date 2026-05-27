#!/home/dan/Chimera_Project/venv/bin/python3
import sys
import os
import json
import subprocess
from datetime import datetime

class WhoisArchiver:
    """
    Agent 08: Domain Registration & Ownership Intelligence.
    Extracts raw registrar data and identifies administrative contacts.
    """
    def __init__(self, domain):
        self.domain = domain
        self.loot_dir = "/home/dan/Chimera_Project/agents/08_Whois_Archiver/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def harvest_whois(self):
        """Executes system whois command for raw data extraction."""
        try:
            # Using subprocess to call system whois for maximum record depth
            result = subprocess.run(['whois', self.domain], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"WHOIS_ERROR: {result.stderr}"
        except Exception as e:
            return f"EXECUTION_ERROR: {str(e)}"

    def parse_intel(self, raw_data):
        """Parses raw text for key infrastructure and contact markers."""
        intel = {
            "domain": self.domain,
            "registrar": "Unknown",
            "emails": [],
            "org": "Private",
            "creation_date": "Unknown",
            "name_servers": []
        }
        
        for line in raw_data.split('\n'):
            line_lower = line.lower().strip()
            if "registrar:" in line_lower:
                intel["registrar"] = line.split(":", 1)[1].strip()
            elif "registrant organization:" in line_lower:
                intel["org"] = line.split(":", 1)[1].strip()
            elif "creation date:" in line_lower or "created on:" in line_lower:
                intel["creation_date"] = line.split(":", 1)[1].strip()
            elif "name server:" in line_lower:
                ns = line.split(":", 1)[1].strip()
                if ns not in intel["name_servers"]:
                    intel["name_servers"].append(ns)
            elif "@" in line_lower and ":" in line_lower:
                # Extract potential contact emails
                potential_email = line.split(":", 1)[1].strip()
                if "@" in potential_email and potential_email not in intel["emails"]:
                    intel["emails"].append(potential_email)
                    
        return intel

    def execute(self):
        print(f"--- [AGENT 08: WHOIS ARCHIVE - {self.domain}] ---")
        raw_intel = self.harvest_whois()
        
        if raw_intel:
            parsed = self.parse_intel(raw_intel)
            
            # Storage Logic
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/whois_{self.domain}_{timestamp}.json"
            
            payload = {
                "timestamp": str(datetime.now()),
                "domain": self.domain,
                "parsed": parsed,
                "raw_data": raw_intel
            }
            
            with open(loot_file, 'w') as f:
                json.dump(payload, f, indent=4)
                
            print(f"[*] DATA STORED: {loot_file}")
            print(f"[*] REGISTRAR: {parsed['registrar']}")
            print(f"[*] NS_COUNT: {len(parsed['name_servers'])}")
            return payload
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
        
    WhoisArchiver(sys.argv[1]).execute()
