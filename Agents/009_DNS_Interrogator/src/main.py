#!/home/dan/Chimera_Project/venv/bin/python3
import dns.resolver
import sys
import os
import json
from datetime import datetime

class DNSInterrogator:
    """
    Agent 09: Advanced DNS Infrastructure Mapper.
    Queries MX, TXT, NS, and SOA records to map mail providers, 
    cloud trust relationships, and SPF/DMARC security policies.
    """
    def __init__(self, domain):
        self.domain = domain
        self.loot_dir = "/home/dan/Chimera_Project/agents/09_DNS_Interrogator/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5
        self.intel = {}

    def query_record(self, rtype):
        """Perform a low-level query for a specific DNS record type."""
        try:
            answers = self.resolver.resolve(self.domain, rtype)
            return [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
            return []
        except Exception as e:
            print(f"[!] Error querying {rtype}: {e}")
            return []

    def execute(self):
        print(f"--- [AGENT 09: DNS INFRASTRUCTURE INTERROGATION - {self.domain}] ---")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        for rtype in record_types:
            print(f"[*] Querying {rtype} records...")
            results = self.query_record(rtype)
            if results:
                self.intel[rtype] = results
                for r in results:
                    print(f"    [>] {r}")

        # Post-processing: Identify Mail Providers from MX
        if 'MX' in self.intel:
            for mx in self.intel['MX']:
                if 'google' in mx.lower(): print("[!] Target utilizes Google Workspace.")
                if 'outlook' in mx.lower(): print("[!] Target utilizes Microsoft 365.")

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/dns_{self.domain}_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump({
                "timestamp": str(datetime.now()),
                "domain": self.domain,
                "records": self.intel
            }, f, indent=4)
            
        print(f"[!!!] DNS INTELLIGENCE COMMITTED: {loot_file}")
        return self.intel

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <domain>")
        sys.exit(1)
        
    DNSInterrogator(sys.argv[1]).execute()
