#!/usr/bin/env python3
import subprocess
import sys
import os
import json

def scan_registry(target_host, port=5000):
    print(f"[*] [Agent 25] Registry-Ransacker: Probing {target_host}:{port}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "registry_catalog.txt")
    
    url = f"http://{target_host}:{port}/v2/_catalog"
    
    try:
        # Use curl to check if the registry API is open and returns JSON
        # -f fails silently on server errors to avoid garbage output
        output = subprocess.check_output(
            ["curl", "-s", "-f", "-L", "--connect-timeout", "3", url],
            stderr=subprocess.DEVNULL
        ).decode()
        
        if output:
            data = json.loads(output)
            repositories = data.get("repositories", [])
            
            if repositories:
                msg = f"[!] CRITICAL: Unauthenticated Registry Found! {len(repositories)} repos discovered."
                print(msg)
                
                with open(loot_path, "w") as f:
                    f.write(f"Registry: {target_host}:{port}\n")
                    f.write("--- Repositories ---\n")
                    for repo in repositories:
                        f.write(f"- {repo}\n")
                
                print(f"[*] Repository list saved to {loot_path}")
            else:
                print("[-] Registry found, but it appears to be empty.")
        else:
            print("[-] No response or authentication required.")

    except json.JSONDecodeError:
        print("[!] Found a service, but it doesn't look like a Docker V2 Registry.")
    except Exception:
        print(f"[-] Could not connect to registry on {target_host}:{port}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_ip> [port]")
        sys.exit(1)
    
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 5000
    scan_registry(target, port)
