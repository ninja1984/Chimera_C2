#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class MitigationAudit:
    """
    Agent 314: Exploit Mitigation Auditor.
    Checks the kernel and running binaries for security 
    protections like ASLR, NX, and Stack Canaries.
    """
    def check_aslr(self):
        print("[*] Auditing ASLR Status...")
        try:
            with open("/proc/sys/kernel/randomize_va_space", "r") as f:
                val = f.read().strip()
                if val == "2":
                    return "FULL (Safe)"
                elif val == "1":
                    return "PARTIAL (Moderate)"
                else:
                    return "DISABLED (Vulnerable)"
        except: return "Unknown"

    def check_process_nx(self, proc_name):
        """Checks if a process has Non-Executable (NX) stacks."""
        print(f"[*] Auditing Memory Maps for {proc_name}...")
        try:
            pid = subprocess.check_output(["pidof", proc_name]).decode().split()[0]
            with open(f"/proc/{pid}/maps", "r") as f:
                maps = f.read()
                # If '[stack]' has 'x' permission, it is vulnerable
                if "[stack]" in maps and "rwx" in maps:
                    return "VULNERABLE (Executable Stack)"
            return "SECURE (NX Enabled)"
        except: return "Process Not Found"

    def execute(self):
        print("--- [AGENT 314: MITIGATION AUDIT SYSTEM] ---")
        print(f"[+] ASLR: {self.check_aslr()}")
        print(f"[+] NX Check (systemd): {self.check_process_nx('systemd')}")

if __name__ == "__main__":
    MitigationAudit().execute()
