#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
import time
from datetime import datetime

class IPSFingerprinter:
    """
    Agent 103: IPS & Network Firewall Fingerprinter.
    Sends known 'Trigger' signatures and monitors for immediate IP 
    shunning or port filtering behavior.
    """
    def __init__(self, target, port=80):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/103_IPS_Fingerprinter/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        
        # Known 'Safe' Trigger: A classic buffer overflow NOP sled signature 
        # that doesn't actually exploit anything but triggers most IDS/IPS.
        self.trigger = b"GET / " + b"\x90" * 100 + b"HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n"

    def check_port_status(self):
        """Simple TCP SYN check to see if the port is reachable."""
        try:
            with socket.create_connection((self.target, self.port), timeout=2):
                return "OPEN"
        except (socket.timeout, ConnectionRefusedError):
            return "FILTERED/CLOSED"
        except Exception:
            return "ERROR"

    def execute(self):
        print(f"--- [AGENT 103: IPS FINGERPRINTING - {self.target}] ---")
        
        # 1. Verify Baseline
        print("[*] Verifying baseline connectivity...")
        baseline = self.check_port_status()
        if baseline != "OPEN":
            print(f"[-] Target port {self.port} is already closed. Aborting.")
            return None

        # 2. Send IPS Trigger
        print(f"[*] Sending IPS Trigger signature to {self.target}:{self.port}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((self.target, self.port))
                s.sendall(self.trigger)
                # Wait for the IPS to process and update firewall rules
                time.sleep(2)
        except Exception as e:
            print(f"    [!] Trigger failed: {e}")

        # 3. Verify Change
        print("[*] Re-checking port status after trigger...")
        post_trigger = self.check_port_status()
        
        detection = "NONE"
        if post_trigger == "FILTERED/CLOSED":
            detection = "ACTIVE_IPS_SHUN"
            print("[!!!] DETECTED: Active IPS/Firewall shunt engaged.")
        else:
            print("[+] No automated network-level blocking detected.")

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/ips_{self.target}_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump({
                "target": self.target,
                "port": self.port,
                "baseline": baseline,
                "post_trigger": post_trigger,
                "detection": detection
            }, f, indent=4)
            
        return detection

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port]")
        sys.exit(1)
        
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 80
    IPSFingerprinter(target, port).execute()
