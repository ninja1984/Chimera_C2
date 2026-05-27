#!/usr/bin/env python3
import platform
import os
import sys
import subprocess

def fingerprint_host():
    print("[*] [Agent 85] Host-Fingerprinter: Extracting system environment details...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "system_info.txt")
    
    info = {
        "OS": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "Distribution": "Unknown"
    }

    # Try to get specific Linux Distro info
    if os.path.exists("/etc/os-release"):
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        info["Distribution"] = line.split("=")[1].strip().replace('"', '')
        except Exception:
            pass

    # Check for Virtualization (Are we in a VM or Container?)
    virt_info = "Physical/Unknown"
    try:
        virt_check = subprocess.check_output(["systemd-detect-virt"], stderr=subprocess.DEVNULL).decode().strip()
        virt_info = virt_check
    except Exception:
        if os.path.exists("/.dockerenv"):
            virt_info = "docker"

    with open(loot_path, "w") as f:
        f.write("--- Host Fingerprint Report ---\n")
        for k, v in info.items():
            f.write(f"{k}: {v}\n")
        f.write(f"Virtualization: {virt_info}\n")
        
    print(f"[+] Fingerprint complete. OS identified as: {info['Distribution']}")
    print(f"[*] Results saved to {loot_path}")

if __name__ == "__main__":
    # Local-only execution
    fingerprint_host()
