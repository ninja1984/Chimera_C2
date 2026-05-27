#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class BannerGrabberPro:
    """
    Agent 10: High-Concurrency Service Identifier.
    Performs protocol-agnostic banner grabbing across multiple ports.
    Uses a Passive-Active probe cycle to bypass simple anti-grab buffers.
    """
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports if isinstance(ports, list) else [ports]
        self.loot_dir = "/home/dan/Chimera_Project/agents/10_Banner_Grabber_Pro/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.results = {}

    def _grab(self, port):
        """Individual socket probe logic."""
        port = int(port)
        banner = "TIMEOUT/NO_RESPONSE"
        try:
            with socket.create_connection((self.target, port), timeout=3) as s:
                # Phase 1: Passive Wait (Some services like SSH/FTP speak first)
                s.settimeout(2)
                try:
                    banner = s.recv(1024).decode(errors='ignore').strip()
                except socket.timeout:
                    # Phase 2: Active Probe (Trigger services like HTTP/SMTP)
                    s.sendall(b"\r\n\r\n")
                    banner = s.recv(1024).decode(errors='ignore').strip()
                
                if banner:
                    print(f"    [+] PORT {port}: {banner[:50]}...")
                    return port, banner
        except Exception:
            pass
        return port, None

    def execute(self, threads=10):
        print(f"--- [AGENT 10: BANNER GRABBING - {self.target}] ---")
        print(f"[*] Targeting {len(self.ports)} ports with {threads} threads...")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_port = {executor.submit(self._grab, p): p for p in self.ports}
            for future in future_to_port:
                port, banner = future.result()
                if banner:
                    self.results[port] = banner

        # Intelligence Commitment
        if self.results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/banners_{self.target}_{timestamp}.json"
            
            payload = {
                "timestamp": str(datetime.now()),
                "target": self.target,
                "banners": self.results
            }
            
            with open(loot_file, 'w') as f:
                json.dump(payload, f, indent=4)
            
            print(f"[!!!] SERVICE INTELLIGENCE COMMITTED: {loot_file}")
            return self.results
        else:
            print("[-] No clear banners retrieved.")
            return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port1,port2...]")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    # Handle comma-separated port list or single port
    port_input = sys.argv[2].split(',') if len(sys.argv) > 2 else [21, 22, 25, 80, 443, 445, 3306, 3389, 8080]
    
    grabber = BannerGrabberPro(target_ip, port_input)
    grabber.execute()
