#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import sys
import os
import json
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime

class MetadataExfiltrator:
    """
    Agent 15: Document Metadata Harvester.
    Crawls target for public documents and extracts internal usernames, 
    software versions, and directory paths from metadata.
    """
    def __init__(self, target_url):
        self.target = target_url.rstrip('/')
        self.loot_dir = "/home/dan/Chimera_Project/agents/15_Metadata_Exfiltrator/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.extensions = ['.pdf', '.docx', '.xlsx', '.pptx']
        self.found_files = []

    def find_docs(self):
        """Scrapes the index page for document links."""
        print(f"[*] AGENT 15: Scanning {self.target} for public documents...")
        try:
            r = requests.get(self.target, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and any(href.endswith(ext) for ext in self.extensions):
                    full_url = href if href.startswith('http') else f"{self.target}/{href.lstrip('/')}"
                    self.found_files.append(full_url)
        except Exception as e:
            print(f"    [!] Scrape Failed: {e}")

    def extract_metadata(self, file_url):
        """Downloads file and runs exiftool for raw metadata extraction."""
        file_name = file_url.split('/')[-1]
        local_path = f"{self.loot_dir}/{file_name}"
        
        try:
            # Download file
            resp = requests.get(file_url, stream=True, timeout=10)
            with open(local_path, 'wb') as f:
                f.write(resp.content)
            
            # Run exiftool (Standard in security environments)
            result = subprocess.run(['exiftool', '-j', local_path], capture_output=True, text=True)
            if result.returncode == 0:
                meta = json.loads(result.stdout)[0]
                # Cleanup: remove the binary file once metadata is harvested
                os.remove(local_path)
                return meta
        except Exception as e:
            print(f"    [!] Metadata extraction failed for {file_name}: {e}")
        return None

    def execute(self):
        print(f"--- [AGENT 15: METADATA EXFILTRATION - {self.target}] ---")
        self.find_docs()
        
        if not self.found_files:
            print("[-] No public documents discovered.")
            return

        print(f"[*] Extracting intelligence from {len(self.found_files)} files...")
        all_metadata = []
        for url in self.found_files:
            meta = self.extract_metadata(url)
            if meta:
                all_metadata.append(meta)
                print(f"    [+] HARVESTED: {url.split('/')[-1]}")

        # Commit to Loot
        if all_metadata:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/metadata_dump_{timestamp}.json"
            with open(loot_file, 'w') as f:
                json.dump(all_metadata, f, indent=4)
            print(f"[!!!] DOCUMENT INTELLIGENCE COMMITTED: {loot_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <http://target.com>")
        sys.exit(1)
        
    MetadataExfiltrator(sys.argv[1]).execute()
