import subprocess
import os
import sys

class HashCracker:
    """
    Chimera Agent 30: Hash Cracker
    Purpose: Automated password cracking using common wordlists.
    """
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.agent_root = os.path.dirname(self.script_dir)
        self.loot_dir = os.path.join(self.agent_root, "loot")
        # Standard Kali wordlist path
        self.wordlist = "/usr/share/wordlists/rockyou.txt"

    def crack_with_john(self, hash_file):
        """Invokes John the Ripper to crack the provided hash file."""
        print(f"[*] Agent 30: Engaging John the Ripper on {hash_file}...")
        
        if not os.path.exists(self.wordlist):
            print("[!] Error: rockyou.txt not found. Run 'gunzip /usr/share/wordlists/rockyou.txt.gz'")
            return

        cmd = ["john", f"--wordlist={self.wordlist}", hash_file]
        
        try:
            subprocess.run(cmd, check=True)
            # Show the results
            print("\n[!!!] Agent 30: CRACKING ATTEMPT COMPLETE. Results:")
            subprocess.run(["john", "--show", hash_file])
        except Exception as e:
            print(f"[!] Agent 30: Cracking failed: {e}")

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 30 :: HASH CRACKER :: CHIMERA SWARM")
        print("="*60)
        print("1. Crack Hash File (John the Ripper)")
        print("2. Check rockyou.txt Status")
        print("0. Return to Commander")
        
        choice = input("\nSelect Action > ")
        
        if choice == "1":
            target_hash = input("Enter path to hash file: ")
            if os.path.exists(target_hash):
                self.crack_with_john(target_hash)
            else:
                print("[!] File not found.")
        elif choice == "2":
            if os.path.exists(self.wordlist):
                print(f"[+] Wordlist found at {self.wordlist}")
            else:
                print("[-] Wordlist missing or compressed (.gz).")
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    cracker = HashCracker()
    cracker.menu()
