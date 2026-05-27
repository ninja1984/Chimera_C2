import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[31m" + "="*60)
    print("   CHIMERA AGENT 36 :: BLOODHOUND AD INGESTOR")
    print("="*60 + "\033[0m")

    domain = input("[?] Target Domain (e.g., internal.corp): ").strip()
    username = input("[?] Domain Username: ").strip()
    password = input("[?] Password: ").strip()
    dc_ip = input("[?] Domain Controller IP: ").strip()

    # Create a target-specific loot folder for the JSON files
    output_dir = f"/home/dan/Chimera_Project/loot/ad_{domain}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"[*] Starting BloodHound ingestion for {domain}...")

    # Using the python implementation of BloodHound (already in your venv)
    # -c All: Collects Users, Groups, Computers, Trusts, ACLs, etc.
    cmd = (
        f"bloodhound-python -u {username} -p {password} "
        f"-d {domain} -dc {dc_ip} -c All --zip "
        f"-o {output_dir}"
    )

    try:
        # We run it and capture output
        process = subprocess.run(cmd.split(), capture_output=True, text=True)
        
        if process.returncode == 0:
            print(f"\033[92m[+] SUCCESS: AD Data collected and zipped in {output_dir}\033[0m")
            db.report_finding("36_BloodHound_Ingestor", "AD_Data_Ingested", {
                "domain": domain,
                "output_path": output_dir,
                "status": "Success"
            })
        else:
            print(f"\033[91m[!] Ingestion Failed: {process.stderr}\033[0m")
            
    except Exception as e:
        print(f"\033[91m[!] Error executing bloodhound-python: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
