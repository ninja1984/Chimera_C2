#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
from datetime import datetime

class TTLExpirator:
    """
    Agent 106: Network Defense Distance Mapper.
    Uses incrementing TTL values to identify the hop count 
    of filtering devices and transparent proxies.
    """
    def __init__(self, target, port=80):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/106_TTL_Expirator/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def probe_distance(self, max_hops=30):
        """Iteratively increases TTL to find the hop where filtering begins."""
        print(f"[*] AGENT 106: Tracing Defense Distance to {self.target}...")
        
        hop_results = []
        for ttl in range(1, max_hops + 1):
            try:
                # Create a raw-ish TCP socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
                s.settimeout(2)
                
                start_time = datetime.now()
                result = s.connect_ex((self.target, self.port))
                end_time = datetime.now()
                
                # Logic: 0 = Success, 11 = Resource temporarily unavailable (likely ICMP timeout)
                status = "REACHED" if result == 0 else "EXPIRED/FILTERED"
                latency = (end_time - start_time).total_seconds() * 1000
                
                hop_results.append({"hop": ttl, "status": status, "latency_ms": latency})
                print(f"    [Hop {ttl}] Status: {status} | Latency: {latency:.2f}ms")
                
                if result == 0:
                    print(f"[+] Target reached at {ttl} hops.")
                    break
                s.close()
            except Exception as e:
                print(f"    [Hop {ttl}] Error: {e}")
        
        return hop_results

    def execute(self):
        print(f"--- [AGENT 106: TTL DEFENSE MAPPING - {self.target}] ---")
        path_data = self.probe_distance()
        
        # Intelligence Commitment
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/ttl_map_{self.target}_{timestamp}.json"
        
        payload = {
            "target": self.target,
            "port": self.port,
            "path": path_data,
            "timestamp": str(datetime.now())
        }
        
        with open(loot_file, 'w') as f:
            json.dump(payload, f, indent=4)
            
        print(f"[!!!] NETWORK TOPOLOGY LOGGED: {loot_file}")
        return path_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port]")
        sys.exit(1)
        
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 80
    TTLExpirator(target, port).execute()
