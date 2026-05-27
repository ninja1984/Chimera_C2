#!/usr/bin/env python3
import subprocess
import sys
import os

def profile_proxy(target_url):
    # Ensure the URL has a protocol
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url
        
    print(f"[*] [Agent 26] Proxy-Profiler: Identifying infrastructure for {target_url}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "proxy_profile.txt")
    
    try:
        # Use curl to get all headers (-i) and follow redirects (-L)
        # We look specifically for 'Server', 'X-Powered-By', and 'Via' headers
        output = subprocess.check_output(
            ["curl", "-s", "-i", "-L", "--connect-timeout", "3", target_url],
            stderr=subprocess.DEVNULL
        ).decode()
        
        headers = [line for line in output.split("\n") if ":" in line]
        interesting_headers = []
        
        # Keywords that indicate proxy or load balancer presence
        proxy_sigs = ["nginx", "haproxy", "traefik", "cloudfront", "cloudflare", "akamai", "via", "x-cache"]
        
        for h in headers:
            if any(sig in h.lower() for sig in proxy_sigs):
                interesting_headers.append(h.strip())

        with open(loot_path, "w") as f:
            f.write(f"Target: {target_url}\n")
            if interesting_headers:
                print(f"[!] Proxy/Infrastructure Detected:")
                for ih in interesting_headers:
                    print(f"    -> {ih}")
                    f.write(ih + "\n")
            else:
                f.write("No obvious proxy headers detected. Direct connection likely.")
                print("[-] No obvious proxy signatures found.")

        print(f"[*] Analysis complete. Results saved to {loot_path}")

    except Exception as e:
        print(f"[!] Profiling failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_url>")
        sys.exit(1)
    
    profile_proxy(sys.argv[1])
