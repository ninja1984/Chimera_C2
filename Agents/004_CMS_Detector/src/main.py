#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import sys
import os
import re

class CMSDetector:
    """
    Agent 04: Content Management System Fingerprinter.
    Analyzes headers, meta-tags, and unique file paths to identify 
    WordPress, Joomla, Drupal, and Ghost installations.
    """
    def __init__(self, target_url):
        self.target = target_url.rstrip('/')
        self.loot_dir = "/home/dan/Chimera_Project/agents/04_CMS_Detector/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

    def detect(self):
        print(f"--- [AGENT 04: CMS FINGERPRINTING - {self.target}] ---")
        try:
            r = requests.get(self.target, headers=self.headers, timeout=10)
            html = r.text
            headers = r.headers
            
            cms_signatures = {
                "WordPress": {
                    "paths": ["/wp-content/", "/wp-includes/", "/wp-json/"],
                    "meta": ["generator\" content=\"WordPress"],
                    "headers": ["x-powered-by"]
                },
                "Joomla": {
                    "paths": ["/administrator/", "/components/", "/modules/"],
                    "meta": ["generator\" content=\"Joomla"],
                    "headers": []
                },
                "Drupal": {
                    "paths": ["/sites/default/", "/core/"],
                    "meta": ["Generator\" content=\"Drupal"],
                    "headers": ["X-Drupal-Cache", "X-Generator"]
                },
                "Ghost": {
                    "paths": ["/ghost/", "content/images/"],
                    "meta": ["generator\" content=\"Ghost"],
                    "headers": []
                }
            }

            detected = "Unknown"
            confidence = 0

            for cms, sigs in cms_signatures.items():
                match_count = 0
                # Check Meta Tags
                for meta in sigs["meta"]:
                    if meta in html: match_count += 2
                
                # Check Paths
                for path in sigs["paths"]:
                    test_r = requests.get(f"{self.target}{path}", headers=self.headers, timeout=5)
                    if test_r.status_code in [200, 403]:
                        match_count += 1
                
                if match_count > confidence:
                    confidence = match_count
                    detected = cms

            if confidence > 0:
                print(f"[!!!] CMS IDENTIFIED: {detected} (Confidence Score: {confidence})")
                self.save_loot(detected, confidence)
                return detected
            else:
                print("[-] CMS could not be definitively identified.")
                return None

        except Exception as e:
            print(f"[!] Fingerprinting Error: {e}")
            return None

    def save_loot(self, cms, score):
        loot_file = f"{self.loot_dir}/id_{self.target.replace('://', '_').replace('/', '_')}.txt"
        with open(loot_file, 'w') as f:
            f.write(f"Target: {self.target}\nDetected CMS: {cms}\nConfidence: {score}\n")
        print(f"[+] Intelligence Committed: {loot_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <http://target.com>")
        sys.exit(1)
    
    detector = CMSDetector(sys.argv[1])
    detector.detect()
