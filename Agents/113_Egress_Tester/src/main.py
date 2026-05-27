#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
from datetime import datetime

class EgressTester:
    """
    Agent 104: Outbound Firewall Auditor.
    Tests which ports are allowed for outbound (Egress) traffic.
    Critical for selecting Reverse Shell ports in the 200-Series.
    """
    def __init__(self, listener_ip):
        self.listener_ip = listener_ip
        self.loot_dir = "/home/dan/Chimera_Project/agents/104_Egress_Tester/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        # Ports typically left open for 'Business Continuity'
        self.common_egress = [21, 22, 53, 80, 443, 8080, 8443, 587, 25]

    def test_outbound(self, port):
        """Attempts to establish a TCP connection to the listener."""
        try:
            with socket.create_connection((self.listener_ip, port), timeout=2):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            # ConnectionRefused is actually a 'Win' because it means 
            # the packet reached the destination (passed the firewall).
            return True
        except Exception:
            return False

    def execute(self):
        print(f"--- [AGENT 104: EGRESS FIREWALL AUDIT - DEST: {self.listener_ip}] ---")
        
        allowed_ports = []
        for port in self.common_egress:
            print(f"[*] Testing Egress on Port {port}...")
            if self.test_outbound(port):
                print(f"    [+] Port {port} appears OPEN for Egress.")
                allowed_ports.append(port)
            else:
                print(f"    [-] Port {port} is FILTERED.")

        # Intelligence Commitment
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/egress_{self.listener_ip}_{timestamp}.json"
        
        payload = {
            "timestamp": str(datetime.now()),
            "listener": self.listener_ip,
            "open_egress_ports": allowed_ports
        }
        
        with open(loot_file, 'w') as f:
            json.dump(payload, f, indent=4)
            
        print(f"[!!!] EGRESS INTELLIGENCE COMMITTED: {loot_file}")
        return allowed_ports

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <your_listener_ip>")
        sys.exit(1)
        
    EgressTester(sys.argv[1]).execute()
