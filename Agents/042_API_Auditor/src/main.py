#!/usr/bin/env python3
import subprocess
import sys
import os

def audit_api(target_url):
    # Standardize URL
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url
        
    print(f"[*] [Agent 35] API-Auditor: Probing {target_url} for API Documentation...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "api_endpoints.txt")
    
    # Common paths where developers leave API documentation/schemas
    api_paths = [
        "swagger-ui.html", "v1/swagger.json", "v2/swagger.json",
        "swagger/v1/swagger.json", "api/docs", "api/v1/docs",
        "openapi.json", "api/swagger-ui.html", "graphql"
    ]
    
    found_docs = []

    for path in api_paths:
        url = f"{target_url.rstrip('/')}/{path}"
        try:
            # -I for headers, -L for redirects, -s for silent
            output = subprocess.check_output(
                ["curl", "-s", "-I", "-L", "--connect-timeout", "2", url],
                stderr=subprocess.DEVNULL
            ).decode()
            
            if "200 OK" in output:
                msg = f"[!] SUCCESS: API Documentation found at {url}"
                print(msg)
                found_docs.append(msg)
        except Exception:
            continue

    with open(loot_path, "w") as f:
        f.write(f"Target: {target_url}\n")
        if found_docs:
            f.write("\n".join(found_docs))
        else:
            f.write("No common API documentation endpoints discovered.")

    print(f"[*] Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_url>")
        sys.exit(1)
    
    audit_api(sys.argv[1])
