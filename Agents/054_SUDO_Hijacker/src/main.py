import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[91m" + "="*60)
    print("   CHIMERA AGENT 47 :: SUDO PRIV-ESC HIJACKER")
    print("="*60 + "\033[0m")

    print("[*] Checking for sudo-related vulnerabilities...")

    # 1. Check Sudo Version (Looking for Baron Samedit or similar)
    try:
        version_output = subprocess.check_output(["sudo", "--version"]).decode()
        print(f"[*] Detected Sudo Version: {version_output.splitlines()[0]}")
    except:
        print("[!] Sudo not found or accessible.")
        return

    # 2. Check 'sudo -l' (The most common OSCP win)
    # This checks what the current user can run AS ROOT without a password.
    print("[*] Running 'sudo -l' to check for NOPASSWD entries...")
    try:
        # We use 'timeout' because some sudo -l commands hang if they ask for a password
        l_output = subprocess.check_output("sudo -l", shell=True, stderr=subprocess.STDOUT, timeout=2).decode()
        print(f"\033[92m[+] Sudo Rights Found:\n{l_output}\033[0m")
        
        if "NOPASSWD" in l_output:
            print("\033[91m[!!!] HIGH VALUE: NOPASSWD entry detected!\033[0m")
            db.report_finding("47_SUDO_Hijacker", "Sudo_NOPASSWD_Found", {
                "output": l_output,
                "severity": "CRITICAL"
            })
    except:
        print("[-] 'sudo -l' requires a password or is restricted.")

    # 3. Check for LD_PRELOAD
    # If LD_PRELOAD is allowed, we can load a malicious .so file to get root.
    if "env_keep += LD_PRELOAD" in locals().get('l_output', ''):
         print("\033[91m[!!!] VULNERABILITY: LD_PRELOAD is enabled in Sudoers!\033[0m")

    db.close()

if __name__ == "__main__":
    run()
