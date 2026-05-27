import os
import sys
import subprocess

def find_suid_binaries():
    """Finds all SUID binaries on the system."""
    print("[*] Scanning for SUID binaries...")
    try:
        # find / -perm -4000 -type f
        output = subprocess.check_output(["find", "/", "-xdev", "-perm", "-4000", "-type", "f"], stderr=subprocess.DEVNULL)
        return output.decode().splitlines()
    except Exception as e:
        print(f"[-] Scan Error: {e}")
        return []

def fuzz_binary(bin_path):
    """
    Performs a primitive buffer overflow fuzz test on a binary 
    by flooding its arguments and environment.
    """
    print(f"[*] Fuzzing: {bin_path}")
    
    # 10KB payload of 'A's
    payload = "A" * 10000
    
    try:
        # Run binary with oversized argument and environmental variable
        # We use a timeout to prevent hanging on interactive binaries
        env = os.environ.copy()
        env["CHIMERA_FUZZ"] = payload
        
        proc = subprocess.run(
            [bin_path, payload], 
            env=env, 
            capture_output=True, 
            timeout=2
        )
        
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        # Check for Segmentation Fault (Return code -11 on Linux)
        if hasattr(e, 'returncode') and e.returncode == -11:
            print(f"[!!!] CRASH DETECTED: {bin_path} (SIGSEGV)")
            return True
        elif "segmentation fault" in str(e).lower():
            print(f"[!!!] CRASH DETECTED: {bin_path}")
            return True
            
    return False

if __name__ == "__main__":
    bins = find_suid_binaries()
    found_vulns = []

    for b in bins:
        if fuzz_binary(b):
            found_vulns.append(b)
            # Log to project loot
            loot_path = "../../../loot/vulnerability_scan.log"
            with open(loot_path, "a") as log:
                log.write(f"Type: SUID_CRASH | Binary: {b} | Status: VULNERABLE\n")

    if found_vulns:
        print(f"\n[!!!] DISCOVERY COMPLETE: Found {len(found_vulns)} potential entry points.")
    else:
        print("\n[*] Fuzzing complete. No immediate crashes found.")
