#!/usr/bin/env python3
import subprocess
import sys
import os

def check_s3(company_name):
    print(f"[*] [Agent 31] S3-Suspect: Probing for public buckets related to '{company_name}'")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "s3_discovery.txt")
    
    # Common bucket suffixes
    suffixes = ["", "-dev", "-prod", "-backup", "-staging", "-data", "-public", "-archive"]
    found_buckets = []

    for suffix in suffixes:
        bucket_name = f"{company_name}{suffix}"
        # AWS S3 URL format
        url = f"http://{bucket_name}.s3.amazonaws.com"
        
        try:
            # -I for headers, -L for redirects
            # 200 OK means it exists and is likely open
            # 403 Forbidden means it exists but is closed
            # 404 Not Found means it doesn't exist
            output = subprocess.check_output(
                ["curl", "-s", "-I", "--connect-timeout", "2", url],
                stderr=subprocess.DEVNULL
            ).decode()
            
            if "200 OK" in output:
                msg = f"[!] CRITICAL: https://{bucket_name}.s3.amazonaws.com is PUBLICLY ACCESSIBLE"
                print(msg)
                found_buckets.append(msg)
            elif "403 Forbidden" in output:
                msg = f"[+] FOUND: {bucket_name} exists but is ACCESS DENIED (Secure)"
                print(msg)
                found_buckets.append(msg)
                
        except Exception:
            continue

    with open(loot_path, "w") as f:
        f.write(f"Company Query: {company_name}\n")
        if found_buckets:
            f.write("\n".join(found_buckets))
        else:
            f.write("No bucket matches found.")

    print(f"[*] Discovery complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <company_keyword>")
        print("Example: python3 main.py tesla")
        sys.exit(1)
    
    check_s3(sys.argv[1])
