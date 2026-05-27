#!/usr/bin/env python3
import subprocess
import os
import sys

def scan_lotl():
    print("[*] [Agent 192] LOTL-Scanner: Identifying dual-use & SUID binaries...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "lotl_report.txt")
    
    # Expanded 'Living Off The Land' List
    lotl_binaries = [
        "curl", "wget", "nc", "ncat", "socat", "ssh", "scp", "sftp",
        "python3", "python", "perl", "ruby", "lua", "php", "gcc", "g++", "make",
        "docker", "kubectl", "aws", "gcloud", "az", "find", "vim", "nano", "ed",
        "certutil", "powershell", "pwsh", "openssl", "base64", "tar", "zip"
    ]
    
    found_bins = []

    # 1. Check the defined list
    for bin_name in lotl_binaries:
        try:
            path = subprocess.check_output(["which", bin_name], stderr=subprocess.DEVNULL).decode().strip()
            if path:
                found_bins.append(f"[KNOWN] {bin_name}: {path}")
        except subprocess.CalledProcessError:
            continue

    # 2. Search for SUID Binaries (The high-value targets)
    print("[*] Searching for SUID binaries (this may take a moment)...")
    try:
        # Find files with permissions 4000 (SUID) starting from root /
        # We redirect errors to /dev/null to avoid 'Permission Denied' spam
        suid_raw = subprocess.check_output("find / -perm -4000 -type f 2>/dev/null | head -n 20", shell=True).decode().strip()
        for line in suid_raw.split('\n'):
            if line:
                found_bins.append(f"[SUID] {line}")
    except Exception as e:
        found_bins.append(f"[!] SUID Search Error: {e}")

    # Write findings to loot
    with open(loot_path, "w") as f:
        f.write("--- Advanced LOTL & Privilege Escalation Report ---\n")
        if found_bins:
            for item in found_bins:
                f.write(item + "\n")
        else:
            f.write("No significant binaries discovered.")
    
    print(f"[*] Analysis complete. Results saved to {loot_path}")

if __name__ == "__main__":
    scan_lotl()
