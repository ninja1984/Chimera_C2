#!/usr/bin/env python3
import subprocess
import os
import sys

def audit_so_hijacking():
    print("[*] [Agent 156] SO-Hijacker: Scanning for writable library paths...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "so_hijack_audit.txt")
    
    results = []

    # 1. Check LD_LIBRARY_PATH (The most common hijack vector)
    ld_path = os.environ.get("LD_LIBRARY_PATH")
    if ld_path:
        for path in ld_path.split(':'):
            if os.access(path, os.W_OK):
                msg = f"[!] CRITICAL: Writable directory in LD_LIBRARY_PATH: {path}"
                print(msg)
                results.append(msg)

    # 2. Check standard library paths for weak permissions
    common_paths = ["/usr/local/lib", "/opt/lib", "/tmp"]
    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.W_OK):
            msg = f"[+] POTENTIAL: Writable library search path: {path}"
            print(msg)
            results.append(msg)

    # 3. Find SUID binaries and check their dependencies using 'ldd'
    print("[*] Checking SUID dependencies (Top 10)...")
    try:
        suid_find = subprocess.check_output("find /usr/bin /usr/sbin -perm -4000 -type f 2>/dev/null | head -n 10", shell=True).decode().split()
        for bin_path in suid_find:
            ldd_output = subprocess.check_output(["ldd", bin_path], stderr=subprocess.DEVNULL).decode()
            if "not found" in ldd_output:
                msg = f"[!!!] EXPLOITABLE: {bin_path} is missing a library! Drop a malicious .so to escalate."
                print(msg)
                results.append(msg)
    except Exception:
        pass

    with open(loot_path, "w") as f:
        f.write("--- Shared Object Hijacking Audit ---\n")
        if results:
            f.write("\n".join(results))
        else:
            f.write("No immediate shared object hijacking vectors identified.")

    print(f"[*] Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    audit_so_hijacking()
