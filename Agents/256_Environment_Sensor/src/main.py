#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess

class EnvironmentSensor:
    """
    Agent 401: Anti-Analysis & Sandbox Detection.
    Checks for hardware and software artifacts indicating the 
    agent is running in a virtualized or monitored environment.
    """
    def is_virtualized(self):
        """Detects common VM hypervisors via MAC addresses and CPU info."""
        print("[*] Sensing Hardware Environment...")
        
        # Check 1: MAC Address OUI (VirtualBox/VMware/Hyper-V signatures)
        try:
            cmd = "cat /sys/class/net/*/address"
            macs = subprocess.getoutput(cmd).lower()
            vm_ouis = ["08:00:27", "00:05:69", "00:0c:29", "00:50:56", "00:15:5d"]
            for oui in vm_ouis:
                if oui in macs:
                    return True, f"VM MAC Detected: {oui}"
        except: pass

        # Check 2: CPU Core Count (Analysis sandboxes often use only 1-2 cores)
        if os.cpu_count() < 2:
            return True, "Suspiciously Low CPU Count (1 Core)"

        # Check 3: Disk Size (Sandboxes often have < 60GB drives)
        try:
            stat = os.statvfs('/')
            total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
            if total_gb < 50:
                return True, f"Suspiciously Small Disk: {total_gb:.2f}GB"
        except: pass

        return False, "Environment appears to be Bare Metal."

    def execute(self):
        print("--- [AGENT 401: ENVIRONMENT SENSING ACTIVE] ---")
        detected, reason = self.is_virtualized()
        
        if detected:
            print(f"[\033[91mALERT\033[0m] Analysis Environment Detected: {reason}")
            print("[*] TRAP TRIGGERED: Initiating Dormant Mode (Self-Obfuscation).")
            # In a real strike, the agent would sys.exit() or run benign code here.
            return False
        
        print("[\033[92mSAFE\033[0m] No analysis artifacts found. Proceeding with mission.")
        return True

if __name__ == "__main__":
    EnvironmentSensor().execute()
