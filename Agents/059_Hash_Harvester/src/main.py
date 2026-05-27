import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[31m" + "="*60)
    print("   CHIMERA AGENT 52 :: AUTOMATED HASH HARVESTER")
    print("="*60 + "\033[0m")

    hash_file = input("[?] Path to hash file (e.g., loot/shadow.txt): ").strip()
    wordlist = "/home/dan/Chimera_Project/data/wordlists/fastpass.txt"

    if not os.path.exists(hash_file):
        print("[!] File not found.")
        return

    print(f"[*] Starting 'John the Ripper' against {hash_file}...")

    try:
        # Use John to crack hashes
        cmd = f"john --wordlist={wordlist} {hash_file}"
        subprocess.run(cmd.split())

        # Show cracked results
        show_cmd = f"john --show {hash_file}"
        result = subprocess.check_output(show_cmd.split()).decode()

        if result:
            print("\033[92m[+] CRACKED PASSWORDS FOUND:\n" + "="*20 + "\n" + result + "="*20 + "\033[0m")
            db.report_finding("52_Hash_Harvester", "Hashes_Cracked", {
                "source_file": hash_file,
                "raw_cracked_data": result
            })
    except Exception as e:
        print(f"[!] Cracking failed: {e}")

    db.close()

if __name__ == "__main__":
    run()
