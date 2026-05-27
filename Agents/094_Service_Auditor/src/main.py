#!/usr/bin/env python3
import subprocess
import os
import sys

def audit_internal_services():
    print("[*] [Agent 87] Service-Auditor: Mapping internal listening ports...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "internal_services.txt")
    
    results = []
    
    # 1. Use 'ss' (Socket Statistics) to find all listening TCP/UDP ports
    # -l (listening), -n (numeric), -t (tcp), -u (udp), -p (process info)
    try:
        # We try to get process info (-p), which requires high-priv but provides better intel
        ss_cmd = ["ss", "-lntup"]
        output = subprocess.check_output(ss_cmd, stderr=subprocess.STDOUT).decode()
        
        lines = output.split('\n')
        for line in lines:
            if "LISTEN" in line or "UNCONN" in line:
                # Highlight localhost-only services
                if "127.0.0.1" in line or "::1" in line:
                    msg = f"[!] INTERNAL ONLY: {line.strip()}"
                    print(msg)
                    results.append(msg)
                else:
                    results.append(f"[+] PUBLIC/LAN: {line.strip()}")
                    
    except subprocess.CalledProcessError as e:
        # If -p fails due to permissions, run without it
        output = subprocess.check_output(["ss", "-lntu"]).decode()
        results.append("Note: Process info hidden (run as root for more detail)\n" + output)

    with open(loot_path, "w") as f:
        f.write("--- Internal & Localhost Service Report ---\n")
        if results:
            f.write("\n".join(results))
        else:
            f.write("No listening services detected.")

    print(f"[*] Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    audit_internal_services()
