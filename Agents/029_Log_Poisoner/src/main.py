#!/usr/bin/env python3
import os
import sys

def audit_log_poisoning():
    print("[*] [Agent 22] Log-Poisoner: Auditing for log-based RCE vectors...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "log_audit.txt")
    
    # Common logs used for poisoning/LFI-to-RCE
    target_logs = [
        "/var/log/auth.log",
        "/var/log/apache2/access.log",
        "/var/log/httpd/access_log",
        "/var/log/nginx/access.log",
        "/var/log/mail.log",
        "/proc/self/environ"
    ]
    
    results = []

    for log in target_logs:
        if os.path.exists(log):
            # Check if we can read the log
            if os.access(log, os.R_OK):
                msg = f"[!] CRITICAL: {log} is READABLE. Potential LFI-to-RCE vector."
                print(msg)
                results.append(msg)
            
            # Check if we can write to the log (very rare, but devastating)
            if os.access(log, os.W_OK):
                msg = f"[!!!] EMERGENCY: {log} is WRITABLE. Direct poisoning possible."
                print(msg)
                results.append(msg)
        else:
            continue

    with open(loot_path, "w") as f:
        f.write("--- Log Poisoning & LFI Audit Report ---\n")
        if results:
            f.write("\n".join(results))
        else:
            f.write("No common sensitive logs are accessible to the current user.")

    print(f"[*] Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    # This is an internal-only agent for local privilege escalation checks
    audit_log_poisoning()
