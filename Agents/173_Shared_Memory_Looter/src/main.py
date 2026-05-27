#!/usr/bin/env python3
import subprocess
import os
import sys

def loot_shared_memory():
    print("[*] [Agent 160] Shared-Memory-Looter: Auditing IPC shared memory segments...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "shm_report.txt")
    
    results = []

    # 1. Use 'ipcs' to list Shared Memory segments
    # Inter-Process Communication (IPC) is how programs talk
    try:
        ipcs_output = subprocess.check_output(["ipcs", "-m"], stderr=subprocess.DEVNULL).decode()
        
        # Look for segments with '666' or '777' permissions (World Readable/Writable)
        lines = ipcs_output.split('\n')
        for line in lines:
            if "666" in line or "777" in line:
                msg = f"[!] VULNERABLE: World-accessible shared memory segment found: {line.strip()}"
                print(msg)
                results.append(msg)
            elif "dest" in line.lower():
                results.append(f"[+] Segment marked for destruction: {line.strip()}")

    except Exception as e:
        print(f"[!] Error accessing IPC info: {e}")

    # 2. Check /dev/shm (The modern way Linux handles shared memory)
    # This is essentially a RAM-disk. People often leave temp files/secrets here.
    shm_path = "/dev/shm"
    if os.path.exists(shm_path):
        files = os.listdir(shm_path)
        for f in files:
            full_path = os.path.join(shm_path, f)
            if os.access(full_path, os.R_OK):
                msg = f"[!] LEAK: Readable file in /dev/shm: {full_path}"
                print(msg)
                results.append(msg)

    with open(loot_path, "w") as f:
        f.write("--- Shared Memory & IPC Audit Report ---\n")
        if results:
            f.write("\n".join(results))
        else:
            f.write("No obvious shared memory vulnerabilities detected.")

    print(f"[*] Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    loot_shared_memory()
