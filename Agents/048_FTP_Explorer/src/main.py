import os
import sys
from ftplib import FTP

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[32m" + "="*60)
    print("   CHIMERA AGENT 41 :: RECURSIVE FTP LOOT EXPLORER")
    print("="*60 + "\033[0m")

    target = input("[?] Target IP: ").strip()
    user = input("[?] FTP Username: ").strip()
    passwd = input("[?] FTP Password: ").strip()

    loot_dir = f"/home/dan/Chimera_Project/loot/ftp_{target}"
    os.makedirs(loot_dir, exist_ok=True)

    try:
        print(f"[*] Connecting to {target}...")
        ftp = FTP(target)
        ftp.login(user=user, passwd=passwd)
        print("\033[92m[+] Login Successful. Indexing files...\033[0m")

        filenames = []
        ftp.retrlines('LIST', filenames.append)

        # High-value targets to look for
        targets = [".ssh", "config", "backup", ".env", "php", "sql", "key"]

        for line in filenames:
            print(f"    {line}")
            for t in targets:
                if t in line.lower():
                    # Extract filename from LIST output (usually last column)
                    fname = line.split()[-1]
                    print(f"\033[91m[!] HIGH VALUE FOUND: {fname}\033[0m")
                    
                    db.report_finding("41_FTP_Explorer", "Sensitive_File_Discovered", {
                        "target": target,
                        "file": fname,
                        "path": "/",
                        "severity": "HIGH"
                    })

        ftp.quit()
    except Exception as e:
        print(f"\033[91m[!] FTP Error: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
