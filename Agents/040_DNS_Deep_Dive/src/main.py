#!/usr/bin/env python3
import subprocess
import sys
import os

def dns_audit(domain):
    print(f"[*] [Agent 33] DNS-Deep-Dive: Auditing {domain} for misconfigurations...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "dns_audit.txt")
    
    results = []

    # 1. Attempt Zone Transfer (AXFR)
    # This is a classic 'Holy Grail' of DNS recon. 
    print("[*] Attempting AXFR Zone Transfer...")
    try:
        # We use 'dig' - a standard Linux networking tool
        axfr_output = subprocess.check_output(
            ["dig", "axfr", f"@{domain}", domain], 
            stderr=subprocess.DEVNULL, timeout=5
        ).decode()
        
        if "Transfer failed" not in axfr_output and len(axfr_output) > 50:
            msg = "[!!!] CRITICAL: DNS Zone Transfer SUCCESSFUL. Full map leaked."
            print(msg)
            results.append(msg + "\n" + axfr_output)
        else:
            print("[-] Zone Transfer refused.")
    except Exception:
        print("[-] Zone Transfer timed out.")

    # 2. Check for TXT Records (Often contain SPF/Office365/Verification keys)
    print("[*] Harvesting TXT records...")
    try:
        txt_output = subprocess.check_output(["dig", "TXT", domain, "+short"]).decode()
        if txt_output:
            results.append("--- TXT Records ---\n" + txt_output)
    except Exception:
        pass

    with open(loot_path, "w") as f:
        f.write(f"Target: {domain}\n")
        if results:
            f.write("\n".join(results))
        else:
            f.write("No major DNS misconfigurations or sensitive records found.")

    print(f"[*] DNS Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <domain>")
        sys.exit(1)
    
    dns_audit(sys.argv[1])
