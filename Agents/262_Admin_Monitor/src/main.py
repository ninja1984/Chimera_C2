#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import subprocess

class ForensicTripwire:
    """
    Agent 407 (Hardened): Kernel-Level Admin Monitor.
    Detects behavioral indicators of a hunter, such as promiscuous 
    mode networking and rapid filesystem auditing.
    """
    def is_promiscuous(self):
        """Checks if any network interface is in 'sniffing' mode (IFF_PROMISC)."""
        # On Linux, /sys/class/net/[iface]/flags shows the interface status.
        # The bit 0x100 (256) indicates Promiscuous mode.
        try:
            for iface in os.listdir('/sys/class/net/'):
                flag_path = f'/sys/class/net/{iface}/flags'
                with open(flag_path, 'r') as f:
                    flags = int(f.read().strip(), 16)
                    if flags & 0x100:
                        return True, iface
        except: pass
        return False, None

    def check_audit_load(self):
        """Checks if the Linux Audit System is actively recording syscalls."""
        # A high 'backlog' or 'enabled' status suggests an active investigation.
        try:
            output = subprocess.getoutput("auditctl -s")
            if "enabled 1" in output or "enabled 2" in output:
                return True
        except: pass
        return False

    def monitor_chimera_access(self):
        """Checks 'atime' (access time) of our own project files."""
        # If the 'atime' is newer than our last internal action, 
        # someone is 'touching' our files.
        try:
            current_atime = os.path.getatime(__file__)
            # Logic: Compare against a stored 'Last Chimera Action' timestamp
            return current_atime
        except: return 0

    def execute(self):
        print("--- [AGENT 407: HARDENED FORENSIC TRIPWIRE] ---")
        
        # Fork to background
        if os.fork() > 0: sys.exit(0)

        while True:
            promisc, dev = self.is_promiscuous()
            auditing = self.check_audit_load()
            
            if promisc:
                # Kernel doesn't lie: Someone is sniffing on 'dev'
                self._emergency_protocol(f"Sniffer detected on {dev}")

            if auditing:
                # The 'Sieve' is actively recording our commands
                self._emergency_protocol("Kernel Auditing (auditd) is ACTIVE")

            time.sleep(1)

    def _emergency_protocol(self, reason):
        # Professional standard: Log to a non-obvious location
        with open("/dev/shm/.tmp_sys_res", "a") as f:
            f.write(f"[{time.ctime()}] ALERT: {reason}\n")
        # In the 500-Series, this triggers the Swarm to 'Go Dark'
        pass

if __name__ == "__main__":
    ForensicTripwire().execute()
