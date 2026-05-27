import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB
from core.logic_engine import ChimeraLogic

def run():
    db = ChimeraDB()
    logic = ChimeraLogic()
    
    os.system('clear')
    print("\033[33m" + "="*60)
    print("   CHIMERA AGENT 23 :: SUDO CONFIGURATION CHECKER")
    print("="*60 + "\033[0m")

    print("[*] Checking 'sudo -l' for current user privileges...")
    
    try:
        # We use -n (non-interactive) to avoid hanging on a password prompt
        cmd = "sudo -ln 2>/dev/null"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        sudo_output = proc.stdout
        
        if not sudo_output:
            print("\033[91m[!] No passwordless sudo entries found for this user.\033[0m")
            return

        print("\033[92m[+] Sudo privileges detected:\033[0m")
        print(f"--- \n{sudo_output} \n---")

        # Parsing the output for binary paths
        # Looking for lines like: (root) NOPASSWD: /usr/bin/find
        for line in sudo_output.splitlines():
            if "NOPASSWD" in line:
                binary_path = line.split(":")[-1].strip().split()[0]
                binary_name = os.path.basename(binary_path)

                # 2. Ask Logic Engine if this is a GTFOBin
                if logic.check_gtfo(binary_name, mode="sudo"):
                    print(f"  \033[91m[CRITICAL] Exploitable Sudo Binary: {binary_name}\033[0m")
                    print(f"      > Vector: sudo {binary_name} [args] -> Root Shell")
                    
                    db.report_finding("23_Sudo_Checker", "Sudo_Exploit", {
                        "binary": binary_name,
                        "path": binary_path,
                        "type": "Sudo_NOPASSWD",
                        "severity": "CRITICAL"
                    })

    except Exception as e:
        print(f"\033[91m[!] Error during Sudo check: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
