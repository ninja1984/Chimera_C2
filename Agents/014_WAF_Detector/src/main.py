#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import sys
import os
import json
from datetime import datetime

class WAFDetector:
    """
    Agent 11: Web Application Firewall Fingerprinter.
    Sends malicious-looking payloads to trigger WAF rejection signatures.
    """
    def __init__(self, target_url):
        self.target = target_url.rstrip('/')
        self.loot_dir = "/home/dan/Chimera_Project/agents/11_WAF_Detector/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Common payloads that trigger WAFs but are harmless to the target
        self.payloads = [
            "/?id=<script>alert(1)</script>",
            "/?file=../../../../etc/passwd",
            "/?user=' OR 1=1 --",
            "/wp-admin/php.ini"
        ]

    def identify_waf(self, response):
        """Analyzes headers and status codes for WAF signatures."""
        headers = response.headers
        code = response.status_code
        
        signatures = {
            "Cloudflare": ["__cfduid", "cf-ray", "cloudflare"],
            "Akamai": ["akamai-gtm", "ak_bmsc"],
            "AWS WAF": ["x-amzn-requestid", "awselb"],
            "ModSecurity": ["mod_security", "NOYB"],
            "Imperva": ["incap_ses", "visid_incap"]
        }

        for waf, sigs in signatures.items():
            for sig in sigs:
                # Check headers and body for signatures
                if sig in str(headers).lower() or sig in response.text.lower():
                    return waf
        
        if code in [403, 406, 501]:
            return "Generic/Unknown WAF (Blocked Content)"
            
        return "None Detected"

    def execute(self):
        print(f"--- [AGENT 11: WAF FINGERPRINTING - {self.target}] ---")
        
        detection_results = {}
        for p in self.payloads:
            url = f"{self.target}{p}"
            try:
                r = requests.get(url, headers=self.headers, timeout=5)
                waf = self.identify_waf(r)
                if waf != "None Detected":
                    detection_results[p] = waf
                    print(f"    [!] DETECTED: {waf} on payload {p}")
            except Exception as e:
                print(f"    [!] Connection Error on {p}: {e}")

        # Final Intelligence
        final_waf = "None"
        if detection_results:
            # Get the most frequently detected WAF
            final_waf = max(set(detection_results.values()), key=list(detection_results.values()).count)
            print(f"[!!!] PRIMARY WAF IDENTIFIED: {final_waf}")
        else:
            print("[+] No WAF signatures triggered.")

        # Store Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/waf_{self.target.replace('://', '_').replace('/', '_')}.json"
        
        with open(loot_file, 'w') as f:
            json.dump({
                "target": self.target,
                "waf_type": final_waf,
                "raw_hits": detection_results
            }, f, indent=4)
            
        return final_waf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <http://target.com>")
        sys.exit(1)
        
    WAFDetector(sys.argv[1]).execute()
