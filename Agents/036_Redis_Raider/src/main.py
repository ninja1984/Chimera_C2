import os
import sys
import socket

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[31m" + "="*60)
    print("   CHIMERA AGENT 29 :: REDIS RAIDER (UNAUTH ACCESS)")
    print("="*60 + "\033[0m")

    target = input("[?] Target IP: ").strip()
    port = 6379

    print(f"[*] Probing {target}:{port} for unauthenticated access...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((target, port))
        
        # Send the 'INFO' command to see if it responds without a password
        s.send(b"INFO\r\n")
        response = s.recv(1024).decode('utf-8', errors='ignore')

        if "redis_version" in response:
            print("\033[92m[!!!] CRITICAL: Redis is UNAUTHENTICATED!\033[0m")
            
            # Extract some basic info for the DB
            version = "Unknown"
            for line in response.splitlines():
                if "redis_version:" in line:
                    version = line.split(":")[1]

            db.report_finding("29_Redis_Raider", "Redis_Unauth_Access", {
                "target": target,
                "version": version,
                "severity": "CRITICAL",
                "exploit_vector": "SSH_Key_Injection_Possible"
            })
            
            print(f"[*] Version: {version}")
            print("[*] Tactical Note: Try writing a webshell or SSH key to the disk.")
        else:
            print("[*] Redis is active but requires authentication.")

        s.close()
    except Exception as e:
        print(f"\033[93m[!] Could not connect to Redis: {e}\033[0m")

    db.close()

if __name__ == "__main__":
    run()
