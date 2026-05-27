#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
import time
from datetime import datetime

class TimingAnalyzer:
    """
    Agent 105: Firewall Cooldown & Shun Timer Auditor.
    Intentionally triggers a block and measures the duration until 
    the target firewall clears the IP from the 'Drop' list.
    """
    def __init__(self, target, port=80):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/105_Timing_Analyzer/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        # IPS Trigger: Common NOP sled signature
        self.trigger = b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n" + b"\x90" * 200 + b"\r\n\r\n"

    def is_blocked(self):
        """Checks if the port is currently unreachable."""
        try:
            with socket.create_connection((self.target, self.port), timeout=2):
                return False # Not blocked
        except:
            return True # Blocked

    def execute(self, check_interval=60):
        print(f"--- [AGENT 105: SHUN TIMING ANALYSIS - {self.target}] ---")
        
        # 1. Ensure we aren't already blocked
        if self.is_blocked():
            print("[!] Already blocked. Wait for manual clear or cooldown before running.")
            return None

        # 2. Trigger the Shun
        print("[*] Triggering IPS Shun...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((self.target, self.port))
                s.sendall(self.trigger)
        except: pass
        
        time.sleep(5) # Give the IPS time to update rules
        
        if not self.is_blocked():
            print("[-] Trigger failed to cause a block. Target may not have active shun rules.")
            return "NO_SHUN_DETECTED"

        # 3. Monitor for Recovery
        print("[*] Shun confirmed. Starting recovery timer...")
        start_time = datetime.now()
        
        recovered = False
        while not recovered:
            time.sleep(check_interval)
            if not self.is_blocked():
                recovered = True
            else:
                elapsed = (datetime.now() - start_time).seconds // 60
                print(f"    [.] Still blocked... {elapsed} minutes elapsed.")

        duration = (datetime.now() - start_time).seconds
        print(f"[!!!] RECOVERY DETECTED. Total Shun Duration: {duration} seconds.")

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/timing_{self.target}_{timestamp}.json"
        
        payload = {
            "target": self.target,
            "shun_duration_seconds": duration,
            "timestamp": str(datetime.now())
        }
        
        with open(loot_file, 'w') as f:
            json.dump(payload, f, indent=4)
            
        return duration

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port]")
        sys.exit(1)
        
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 80
    TimingAnalyzer(target, port).execute()
