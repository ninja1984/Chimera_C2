#!/usr/bin/env python3
import subprocess
import sys
import os

def crawl_configs(target_url):
    # Ensure the URL has a protocol
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url
        
    print(f"[*] [Agent 14] Config-Crawler: Searching for sensitive files on {target_url}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "leaked_configs.txt")
    
    # Files often left behind by lazy deployment or backups
    sensitive_files = [
        ".env", ".git/config", ".ssh/id_rsa", "config.php.bak",
        "settings.py.old", "database.sql.gz", ".docker/config.json",
        "web.config", "phpinfo.php", ".htaccess"
    ]
    
    leaks = []

    for file_path in sensitive_files:
        url = f"{target_url.rstrip('/')}/{file_path}"
        try:
            # -I sends a HEAD request (stealthier, only gets headers)
            # -L follows redirects
            output = subprocess.check_output(
                ["curl", "-s", "-I", "-L", "--connect-timeout", "2", url], 
                stderr=subprocess.DEVNULL
            ).decode()
            
            # Check for 200 OK (File is there) or 403 Forbidden (Directory exists but blocked)
            if "200 OK" in output:
                msg = f"[!] CRITICAL: {url} is PUBLICLY ACCESSIBLE"
                print(msg)
                leaks.append(msg)
            elif "403 Forbidden" in output:
                msg = f"[+] INTERESTING: {url} exists but is FORBIDDEN"
                print(msg)
                leaks.append(msg)
                
        except Exception:
            continue

    with open(loot_path, "w") as f:
        f.write(f"Target: {target_url}\n")
        if leaks:
            f.write("\n".join(leaks))
        else:
            f.write("No common sensitive files discovered.")

    print(f"[*] Analysis complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_url>")
        sys.exit(1)
    
    crawl_configs(sys.argv[1])
