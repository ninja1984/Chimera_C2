#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess

class CleanupValidator:
    """
    Agent 321: Post-Op Forensic Auditor.
    Actively scans system logs and metadata to ensure Agent 212 
    successfully removed all traces of the Chimera engagement.
    """
    def __init__(self, attacker_ip="10.0.2.15"):
        self.attacker_ip = attacker_ip
        self.targets = [
            "/var/log/auth.log",
            "/var/log/syslog",
            "/var/log/apache2/access.log",
            "/var/log/nginx/access.log",
            "~/.bash_history"
        ]

    def scan_for_traces(self):
        print(f"--- [AGENT 321: ACTIVE CLEANUP VALIDATION] ---")
        print(f"[*] Scanning for traces of IP: {self.attacker_ip}...")
        
        found_traces = []

        for log in self.targets:
            log_path = os.path.expanduser(log)
            if os.path.exists(log_path):
                try:
                    # Search for the IP or 'chimera' string in the logs
                    cmd = f"grep -Ei '{self.attacker_ip}|chimera' {log_path} | head -n 5"
                    result = subprocess.getoutput(cmd)
                    
                    if result:
                        print(f"[\033[91mFAILED\033[0m] Evidence found in {log_path}")
                        found_traces.append(log_path)
                    else:
                        print(f"[\033[92mCLEAN\033[0m] No traces in {log_path}")
                except Exception as e:
                    print(f"[!] Error scanning {log_path}: {e}")

        # Final Verdict
        if not found_traces:
            print("\n[!!!] VERDICT: [VERIFIED CLEAN]. No digital DNA detected.")
            return True
        else:
            print(f"\n[!!!] VERDICT: [FLAGGED]. {len(found_traces)} logs still contain evidence.")
            return False

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else "10.0.2.15"
    CleanupValidator(ip).scan_for_traces()
