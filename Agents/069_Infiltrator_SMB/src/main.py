import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[33m" + "="*60)
    print("   CHIMERA AGENT 62 :: INFILTRATOR_SMB (SHARE HUNTER)")
    print("="*60 + "\033[0m")

    target_ip = input("[?] Target IP to Enum: ").strip()
    
    print(f"[*] Checking for NULL Sessions and Open Shares on {target_ip}...")

    try:
        # Using smbclient to list shares without a password (NULL Session)
        cmd = f"smbclient -L {target_ip} -N"
        shares = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode()
        print(f"\033[92m[+] Shares Discovered:\n{shares}\033[0m")

        # Logic: If 'C$' or 'Backup' or 'Users' is found, flag for deep dive
        if "Disk" in shares:
            print("[!] Found accessible Disk shares. Identifying high-value files...")
            # We'd normally use 'smbmap' or 'crackmapexec' here to spider the files
            db.report_finding("62_Infiltrator_SMB", "SMB_Shares_Accessible", {
                "target": target_ip,
                "shares": shares,
                "severity": "MEDIUM"
            })

    except Exception as e:
        print(f"[-] SMB Enumeration failed: {e}")

    db.close()

if __name__ == "__main__":
    run()
