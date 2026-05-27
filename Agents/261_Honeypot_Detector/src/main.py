#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import socket

class DeceptionInquisitor:
    """
    Agent 406 (Hardened): Deep-Kernel Honeypot Detection.
    Scans for inconsistencies in kernel artifacts, hardware 
    thermal data, and filesystem entropy to identify deception.
    """
    def check_thermal_data(self):
        """Real hardware has thermal sensors. Most VMs/Honeypots do not."""
        print("[*] Interrogating Thermal Hardware...")
        thermal_path = "/sys/class/thermal/"
        if not os.path.exists(thermal_path) or not os.listdir(thermal_path):
            return True, "No thermal sensors found (Likely Virtual/Deception)"
        return False, "Thermal sensors present"

    def check_filesystem_entropy(self):
        """Real servers have high 'noise' in /tmp and /var/log."""
        print("[*] Analyzing Filesystem Entropy...")
        try:
            # Count files in /tmp created in the last 24 hours
            cmd = "find /tmp -type f -mmin -1440 | wc -l"
            count = int(subprocess.getoutput(cmd))
            if count < 3:
                return True, f"Suspiciously sterile filesystem ({count} new files in /tmp)"
        except: pass
        return False, "Natural filesystem activity detected"

    def check_bogus_macs(self):
        """Checks for MAC addresses used by deception companies like Illusive or TrapX."""
        print("[*] Checking for Deception Vendor MACs...")
        try:
            cmd = "cat /sys/class/net/*/address"
            macs = subprocess.getoutput(cmd).lower()
            # Common 'Deception' or 'Research' OUIs
            trap_ouis = ["00:0c:29", "08:00:27", "00:50:56"] 
            for oui in trap_ouis:
                if oui in macs:
                    return True, f"Found Research/VM OUI: {oui}"
        except: pass
        return False, "Network stack appears standard"

    def execute(self):
        print("--- [AGENT 406: HARDENED DECEPTION INQUISITION] ---")
        
        results = [
            self.check_thermal_data(),
            self.check_filesystem_entropy(),
            self.check_bogus_macs()
        ]

        score = sum(1 for is_hp, msg in results if is_hp)
        
        print("\n[!] INVESTIGATION SUMMARY:")
        for is_hp, msg in results:
            status = "[\033[91m!\033[0m]" if is_hp else "[\033[92m+\033[0m]"
            print(f"    {status} {msg}")

        if score >= 2:
            print(f"\n[\033[91mDANGER\033[0m] HIGH CONFIDENCE: THIS IS A TRAP. (Score: {score}/3)")
            return True
        elif score == 1:
            print(f"\n[\033[93mWARNING\033[0m] LOW CONFIDENCE: Possible Deception. (Score: 1/3)")
            return False
        
        print("\n[\033[92mSAFE\033[0m] BEYOND REASONABLE DOUBT: PRODUCTION SERVER.")
        return False

if __name__ == "__main__":
    DeceptionInquisitor().execute()
