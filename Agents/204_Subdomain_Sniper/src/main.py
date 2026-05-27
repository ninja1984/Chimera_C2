#!/usr/bin/env python3
import socket
import sys
import os

def brute_force_dns(target_domain):
    print(f"[*] [Agent 191] Subdomain-Sniper: Sniping {target_domain}")
    
    # Absolute path resolution
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_dir = os.path.join(base_dir, "loot")
    loot_path = os.path.join(loot_dir, "subdomains.txt")

    if not os.path.exists(loot_dir):
        os.makedirs(loot_dir)

    subdomains = ["dev", "staging", "api", "vpn", "mail", "internal", "test", "corp", "db"]
    
    found_count = 0
    for sub in subdomains:
        query = f"{sub}.{target_domain}"
        try:
            ip = socket.gethostbyname(query)
            result = f"[+] FOUND: {query} -> {ip}"
            print(result)
            with open(loot_path, "a") as f:
                f.write(result + "\n")
            found_count += 1
        except socket.gaierror:
            continue

    if found_count == 0:
        print("[-] No common subdomains resolved.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_domain>")
        sys.exit(1)
    
    brute_force_dns(sys.argv[1])
