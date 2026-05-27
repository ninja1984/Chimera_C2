#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import socket
import json
import subprocess
from datetime import datetime

class SystemSurveyor:
    """
    Agent 301: Internal Landscape Cartographer.
    Maps the internal network from a compromised beachhead to 
    identify pivot points and high-value internal assets.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/301_System_Surveyor/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def get_network_interfaces(self):
        """Identifies all active network interfaces and IP ranges."""
        print("[*] Enumerating Network Interfaces...")
        try:
            # Using 'ip addr' for high-fidelity output on modern Linux
            output = subprocess.check_output(["ip", "-o", "addr", "show"]).decode()
            return output
        except Exception:
            return "Could not retrieve interface data."

    def get_arp_cache(self):
        """Finds other machines the host has recently communicated with."""
        print("[*] Extracting ARP Cache (Neighborhood Intelligence)...")
        try:
            return subprocess.check_output(["ip", "neigh", "show"]).decode()
        except Exception:
            return "Could not retrieve ARP data."

    def internal_port_scan(self, subnet_prefix):
        """Performs a lightweight 'Connect Scan' on the local subnet."""
        # Note: We only scan for 80, 443, 445 (SMB), and 22 (SSH) to keep it quiet
        common_ports = [22, 80, 443, 445]
        found_hosts = []
        
        print(f"[*] Surveying Subnet: {subnet_prefix}.0/24...")
        for i in range(1, 254):
            target = f"{subnet_prefix}.{i}"
            for port in common_ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.01) # Ultra-fast timeout for local noise reduction
                result = s.connect_ex((target, port))
                if result == 0:
                    print(f"    [+] Found Active Service: {target}:{port}")
                    found_hosts.append({"ip": target, "port": port})
                s.close()
        return found_hosts

    def execute(self, subnet_to_scan=None):
        print("--- [AGENT 301: SYSTEM SURVEYOR ACTIVE] ---")
        
        survey_data = {
            "timestamp": str(datetime.now()),
            "interfaces": self.get_network_interfaces(),
            "neighbors": self.get_arp_cache(),
            "discovered_assets": []
        }

        if subnet_to_scan:
            survey_data["discovered_assets"] = self.internal_port_scan(subnet_to_scan)

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/survey_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump(survey_data, f, indent=4)
            
        print(f"[!!!] SURVEY COMPLETE. MAP STORED AT: {loot_file}")

if __name__ == "__main__":
    # Example: If the host is 10.0.2.15, scan 10.0.2
    sub = sys.argv[1] if len(sys.argv) > 1 else None
    SystemSurveyor().execute(sub)
