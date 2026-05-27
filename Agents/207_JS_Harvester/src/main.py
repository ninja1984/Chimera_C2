#!/usr/bin/env python3
import re
import sys
import os
import subprocess

def harvest_js(target_url):
    print(f"[*] [Agent 194] JS-Harvester: Analyzing {target_url}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "js_secrets.txt")
    
    # Regex for common high-value strings
    patterns = {
        "API_Key": r"(['\"]|)(?:api_key|apikey|key|secret)(['\"]|)\s*[:=]\s*(['\"])([A-Za-z0-9-_]{16,40})\3",
        "Endpoint": r"(['\"])(https?://[\w\.-]+(?:/[\w\.-]*)*)\1",
        "Firebase": r"[\w-]+\.firebaseio\.com",
        "AWS_Key": r"AKIA[0-9A-Z]{16}"
    }

    try:
        # Using curl to grab the page source (LOTL technique)
        raw_html = subprocess.check_output(["curl", "-s", "-L", target_url], stderr=subprocess.DEVNULL).decode()
        
        found_data = []
        for name, pattern in patterns.items():
            matches = re.findall(pattern, raw_html)
            for m in matches:
                # regex findall returns tuples if there are multiple groups
                val = m[3] if isinstance(m, tuple) and len(m) > 3 else str(m)
                print(f"[!] POTENTIAL {name}: {val}")
                found_data.append(f"{name}: {val}")

        with open(loot_path, "w") as f:
            f.write(f"Source: {target_url}\n")
            f.write("\n".join(set(found_data))) # Set to unique values
            
        print(f"[*] Harvest complete. Loot saved to {loot_path}")

    except Exception as e:
        print(f"[!] Harvesting failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_url>")
        sys.exit(1)
    harvest_js(sys.argv[1])
