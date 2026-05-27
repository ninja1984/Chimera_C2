#!/usr/bin/env python3
import subprocess
import sys
import os

def watch_winrm(target_ip):
    print(f"[*] [Agent 28] WinRM-Watcher: Probing {target_ip} for Management Endpoints")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "winrm_discovery.txt")
    
    # WinRM Ports: 5985 (HTTP), 5986 (HTTPS)
    ports = ["5985", "5986"]
    found_endpoints = []

    for port in ports:
        try:
            # We use curl to probe the WS-Management path
            # If WinRM is active, it usually returns a 401 or 405 with specific headers
            url = f"http://{target_ip}:{port}/wsman" if port == "5985" else f"https://{target_ip}:{port}/wsman"
            
            output = subprocess.check_output(
                ["curl", "-s", "-I", "-k", "--connect-timeout", "2", url],
                stderr=subprocess.DEVNULL
            ).decode()
            
            if "401" in output or "405" in output:
                auth_types = []
                if "Negotiate" in output: auth_types.append("Negotiate/Kerberos")
                if "NTLM" in output: auth_types.append("NTLM")
                if "Basic" in output: auth_types.append("Basic (VULNERABLE)")
                
                msg = f"[!] FOUND: WinRM on Port {port}. Auth: {', '.join(auth_types) if auth_types else 'Unknown'}"
                print(msg)
                found_endpoints.append(msg)
                
        except Exception:
            continue

    with open(loot_path, "w") as f:
        f.write(f"Target: {target_ip}\n")
        if found_endpoints:
            f.write("\n".join(found_endpoints))
        else:
            f.write("No WinRM endpoints detected.")

    print(f"[*] Analysis complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_ip>")
        sys.exit(1)
    
    watch_winrm(sys.argv[1])
