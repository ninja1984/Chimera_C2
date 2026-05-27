#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import json
import socket
import struct
from datetime import datetime

class InterfaceIntrospector:
    """
    Agent 05: Local Network Topology Mapper.
    Extracts deep interface metadata, ARP tables, and routing logic
    directly from system primitives to identify lateral movement paths.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/05_Interface_Introspector/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.intel = {
            "interfaces": {},
            "routes": [],
            "arp_cache": []
        }

    def _get_flags(self, flags_hex):
        """Decodes interface flags from /proc/net/dev format."""
        # Simple mapping for UP/RUNNING/PROMISC etc.
        flags = int(flags_hex, 16)
        res = []
        if flags & 0x1: res.append("UP")
        if flags & 0x2: res.append("BROADCAST")
        if flags & 0x100: res.append("PROMISC")
        return res

    def harvest_interfaces(self):
        """Reads raw interface data from /proc/net/dev and /sys/class/net."""
        print("[*] AGENT 05: Introspecting Network Interfaces...")
        try:
            with open("/proc/net/dev", "r") as f:
                lines = f.readlines()[2:] # Skip headers
                for line in lines:
                    parts = line.split(":")
                    if len(parts) < 2: continue
                    iface = parts[0].strip()
                    
                    # Get MAC and MTU from sysfs
                    mac = "Unknown"
                    mtu = 0
                    try:
                        with open(f"/sys/class/net/{iface}/address", "r") as m:
                            mac = m.read().strip()
                        with open(f"/sys/class/net/{iface}/mtu", "r") as mt:
                            mtu = int(mt.read().strip())
                    except: pass
                    
                    self.intel["interfaces"][iface] = {
                        "mac": mac,
                        "mtu": mtu,
                        "stats": parts[1].split()[:2] # RX/TX bytes
                    }
            print(f"[+] Discovered {len(self.intel['interfaces'])} interfaces.")
        except Exception as e:
            print(f"[!] Interface Harvest Failed: {e}")

    def harvest_routes(self):
        """Parses /proc/net/route to map the gateway and subnets."""
        print("[*] AGENT 05: Mapping Kernel Routing Table...")
        try:
            with open("/proc/net/route", "r") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    p = line.split()
                    if len(p) < 3: continue
                    # Convert hex IP to dotted quad
                    def hex_to_ip(hex_str):
                        return socket.inet_ntoa(struct.pack("<L", int(hex_str, 16)))
                    
                    self.intel["routes"].append({
                        "iface": p[0],
                        "destination": hex_to_ip(p[1]),
                        "gateway": hex_to_ip(p[2]),
                        "mask": hex_to_ip(p[7])
                    })
        except Exception as e:
            print(f"[!] Route Mapping Failed: {e}")

    def execute(self):
        print(f"--- [AGENT 05: INTERFACE INTROSPECTION - LOCALHOST] ---")
        self.harvest_interfaces()
        self.harvest_routes()
        
        # Save Intelligence
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/topology_{timestamp}.json"
        with open(loot_file, "w") as f:
            json.dump(self.intel, f, indent=4)
        
        print(f"[!!!] TOPOLOGY COMMITTED: {loot_file}")
        
        # Print Summary for the Brain
        for iface, data in self.intel["interfaces"].items():
            print(f"    [>] {iface} ({data['mac']}) MTU: {data['mtu']}")
        
        return loot_file

if __name__ == "__main__":
    InterfaceIntrospector().execute()
