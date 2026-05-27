#!/usr/bin/env python3
import subprocess
import sys
import os

def check_takeover(domain):
    print(f"[*] [Agent 39] Subdomain-Takeover-Seeker: Auditing {domain} for dangling CNAMEs")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "takeover_audit.txt")
    
    # Common signatures of "dangling" services
    signatures = {
        "github.io": "There isn't a GitHub Pages site here",
        "herokuapp.com": "herokucdn.com/error-pages/no-such-app.html",
        "cloudfront.net": "Bad Gateway",
        "s3.amazonaws.com": "NoSuchBucket",
        "azurewebsites.net": "404 Web Site not found"
    }

    try:
        # 1. Get the CNAME record
        cname_output = subprocess.check_output(["dig", "CNAME", domain, "+short"]).decode().strip()
        
        if cname_output:
            print(f"[+] Found CNAME: {domain} -> {cname_output}")
            
            # 2. Check the response content for 'missing service' signatures
            # We use curl to see what the page actually says
            page_content = subprocess.check_output(
                ["curl", "-s", "-L", "--connect-timeout", "3", f"http://{domain}"],
                stderr=subprocess.DEVNULL
            ).decode()
            
            vulnerable = False
            for provider, sig in signatures.items():
                if provider in cname_output and sig in page_content:
                    msg = f"[!!!] CRITICAL: POTENTIAL TAKEOVER on {domain} via {provider}"
                    print(msg)
                    vulnerable = True
                    with open(loot_path, "a") as f:
                        f.write(msg + "\n")
            
            if not vulnerable:
                print("[-] CNAME exists but service appears active or claimed.")
        else:
            print("[-] No CNAME record found for this domain.")

    except Exception as e:
        print(f"[!] Error during audit: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <subdomain>")
        sys.exit(1)
    
    check_takeover(sys.argv[1])
