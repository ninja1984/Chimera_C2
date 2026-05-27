#!/usr/bin/env python3
import os
import subprocess
import sys

def audit_container():
    print("[*] [Agent 196] Container-Escaper: Auditing for escape vectors...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "escape_audit.txt")
    
    results = []

    # 1. Check for Privileged Mode
    # If a container is run with --privileged, it has access to host devices.
    if os.path.exists("/dev/sda1"):
        msg = "[!] CRITICAL: Host devices found in /dev/ (Possible Privileged Mode)"
        print(msg)
        results.append(msg)

    # 2. Check for Docker Socket Mount
    # Mounting /var/run/docker.sock allows the container to control the Docker daemon.
    if os.path.exists("/var/run/docker.sock"):
        msg = "[!] CRITICAL: Docker socket found! Escape to host is trivial via 'docker run'."
        print(msg)
        results.append(msg)

    # 3. Check for Sensitive Mounts (proc/sys)
    # Writing to /proc/sys/kernel/core_pattern can lead to escape.
    if os.access("/proc/sys/kernel/core_pattern", os.W_OK):
        msg = "[!] HIGH: /proc/sys/kernel/core_pattern is WRITABLE."
        print(msg)
        results.append(msg)

    # 4. Check capabilities
    try:
        caps = subprocess.check_output(["capsh", "--print"], stderr=subprocess.DEVNULL).decode()
        if "cap_sys_admin" in caps:
            msg = "[!] HIGH: CAP_SYS_ADMIN capability detected."
            print(msg)
            results.append(msg)
    except FileNotFoundError:
        results.append("[?] capsh not found; skipping capability check.")

    with open(loot_path, "w") as f:
        f.write("--- Container Escape Vulnerability Report ---\n")
        f.write("\n".join(results) if results else "No immediate escape vectors identified.")

    print(f"[*] Audit complete. Report: {loot_path}")

if __name__ == "__main__":
    audit_container()
